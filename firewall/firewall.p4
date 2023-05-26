#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;
const bit<8> TYPE_UDP = 0x11;

const bit<8> ZERO   = 0x30; // '0'
const bit<8> ONE    = 0x31; // '1'
const bit<8> TWO    = 0x32; // '2'
const bit<8> THREE  = 0x33; // '3'
const bit<8> FOUR   = 0x34; // '4'
const bit<8> FIVE   = 0x35; // '5'
const bit<8> SIX    = 0x36; // '6'
const bit<8> SEVEN  = 0x37; // '7'
const bit<8> EIGHT  = 0x38; // '8'
const bit<8> NINE   = 0x39; // '9'
const bit<8> DOT    = 0x2e; // '.'


/* HEADERS */
typedef bit<9> egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length_;
    bit<16> checksum;
}

/*
 * All metadata, globally used in the program, also  needs to be assembled
 * into a single struct. As in the case of the headers, we only need to
 * declare the type, but there is no need to instantiate it,
 * because it is done "by the architecture", i.e. outside of P4 functions
 */

struct metadata {
    /* In our case it is empty */
}

struct headers {
    ethernet_t	ethernet;
    ipv4_t	ipv4;
    udp_t	udp;
}

/*************************************************************************
 ***********************  P A R S E R  ***********************************
 *************************************************************************/
parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    state start {
	transition parse_ethernet;
    }
    
    state parse_ethernet {
	packet.extract(hdr.ethernet);
	transition select(hdr.ethernet.etherType) {
	    TYPE_IPV4 : parse_ipv4;
	    default : accept;
	}
    }
    
    state parse_ipv4 {
	packet.extract(hdr.ipv4);
	transition select(hdr.ipv4.protocol) {
	    TYPE_UDP : parse_udp;
	    default : accept;
	}
    }

    state parse_udp {
	packet.extract(hdr.udp);
	transition accept;
    }
}

/*************************************************************************
 ************   C H E C K S U M    V E R I F I C A T I O N   *************
 *************************************************************************/
control MyVerifyChecksum(inout headers hdr,
                         inout metadata meta) {
    apply { }
}

/*************************************************************************
 **************  I N G R E S S   P R O C E S S I N G   *******************
 *************************************************************************/
control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action swap_mac_addresses() {
	macAddr_t tmp;
	tmp = hdr.ethernet.dstAddr;
	hdr.ethernet.dstAddr = hdr.ethernet.srcAddr;
	hdr.ethernet.srcAddr = tmp;
	standard_metadata.egress_spec = standard_metadata.ingress_port;

    action drop() {
        mark_to_drop(standard_metadata);
    }

    // Five-Tuple Implementation
    table ipv4_lpm {
        key = {
	    hdr.ipv4.srcAddr: exact;
            hdr.ipv4.dstAddr: lpm;
	    hdr.ipv4.protocol: exact;
	    hdr.udp.srcPort: exact;
	    hdr.udp.dstPort: exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }

    apply {
        if (hdr.ipv4.isValid() || hdr.ipv4.ttl != 0) {
            ipv4_lpm.apply();
        }
    }
}

/*************************************************************************
 ****************  E G R E S S   P R O C E S S I N G   *******************
 *************************************************************************/
control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

/*************************************************************************
 *************   C H E C K S U M    C O M P U T A T I O N   **************
 *************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {
	update_checksum(
	    hdr.ipv4.isValid(),
	    { hdr.ipv4.version,
          hdr.ipv4.ihl,
          hdr.ipv4.diffserv,
          hdr.ipv4.totalLen,
          hdr.ipv4.identification,
          hdr.ipv4.flags,
          hdr.ipv4.fragOffset,
          hdr.ipv4.ttl,
          hdr.ipv4.protocol,
          hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr
        },
        hdr.ipv4.hdrChecksum,
        HashAlgorithm.csum16);
	}
}

/*************************************************************************
 ***********************  D E P A R S E R  *******************************
 *************************************************************************/
control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.udp);
    }
}

/*************************************************************************
 ***********************  S W I T C H **********************************
 *************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
