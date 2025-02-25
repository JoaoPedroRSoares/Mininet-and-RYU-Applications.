from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4

# Regras de bloqueio com base nos endereços IP (Top-Down)
rules = [
    ('10.0.0.10', '10.1.0.10'),  # Bloqueia h1 <-> h2
    ('10.1.0.10', '10.3.0.10'),  # Bloqueia h2 <-> h4
    ('10.2.0.10', '10.3.0.10')   # Bloqueia h3 <-> h4
]

class SDNFirewall(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNFirewall, self).__init__(*args, **kwargs)
        self.logger.info("Firewall inicializado")

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Instalar regras de bloqueio primeiro (prioridade alta)
        for rule in rules:
            match = parser.OFPMatch(eth_type=0x0800, ipv4_src=rule[0], ipv4_dst=rule[1])
            self.add_flow(datapath, 10, match, [])
            match_reverse = parser.OFPMatch(eth_type=0x0800, ipv4_src=rule[1], ipv4_dst=rule[0])
            self.add_flow(datapath, 10, match_reverse, [])

        # Regra padrão no final (prioridade baixa) para permitir todo o resto
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
        self.add_flow(datapath, 1, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        if ip_pkt:
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst
            self.logger.info(f"Pacote recebido: {src_ip} -> {dst_ip}")

            # Verifica se o tráfego deve ser bloqueado
            for rule in rules:
                if (src_ip == rule[0] and dst_ip == rule[1]) or (src_ip == rule[1] and dst_ip == rule[0]):
                    self.logger.warning(f"Bloqueando tráfego entre {src_ip} e {dst_ip}")
                    return  # Descarta o pacote

            # Se não for bloqueado, segue a regra padrão e permite tráfego
            match = parser.OFPMatch(eth_type=0x0800, ipv4_src=src_ip, ipv4_dst=dst_ip)
            actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
            self.add_flow(datapath, 1, match, actions)

            # Envia o pacote atual
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=msg.data)
            datapath.send_msg(out)
