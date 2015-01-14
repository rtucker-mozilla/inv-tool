from invtool.lib.options import build_extractor, write_num_argument
from invtool.tests.test_data import (
    TEST_DOMAIN, TEST_FQDN, TEST_IPv4, TEST_IPv6, TEST_TTL, TEST_PORT,
    TEST_WEIGHT, TEST_PRIORITY, TEST_TEXT, TEST_INAME
)


def view_arguments(field_name):
    def add_view_arguments(parser, required=False):
        pri_group = parser.add_mutually_exclusive_group()

        pri_group.add_argument('--no-private', default=False,
                               action='store_true', dest='no_private',
                               help="Disable private view.", required=required)

        pri_group.add_argument('--private', default=False, action='store_true',
                               dest='private', help="Enabled private view.",
                               required=False)

        pub_group = parser.add_mutually_exclusive_group()

        pub_group.add_argument('--no-public', default=False,
                               action='store_true', dest='no_public',
                               help="Disable public view.", required=required)

        pub_group.add_argument('--public', default=False, action='store_true',
                               dest='public', help="Enabled public view.",
                               required=False)

    def extract_views(nas):
        views = []
        if nas.no_private:
            views.append('no-private')
        elif nas.private:
            views.append('private')

        if nas.no_public:
            views.append('no-public')
        elif nas.public:
            views.append('public')
        data = {field_name: views}
        return data

    def test_data():
        return '', '--no-public --private'

    return add_view_arguments, extract_views, test_data


def _add_domain_argument(parser, required=True):
    parser.add_argument(
        '--domain', default=None, type=str, dest='domain',
        help="The domain a record is in.", required=False)


def domain_argument(field_name):
    def extract_domain(nas):
        data = {}
        if nas.domain:
            data.update({field_name: nas.domain})
            return data

    def test_data():
        return 'domain', TEST_DOMAIN

    return _add_domain_argument, extract_domain, test_data


def _add_label_argument(parser, required=True):
    parser.add_argument(
        '--label', default="", type=str, dest='label',
        help="The first label in the fqdn. If label is ommited then '' is "
        "used and is analigouse to using '@' in a zone file (the record "
        "will get it's domain's name as it's fqdn).", required=False
    )


def fqdn_argument(field_name, rdtype):
    # We need rdtype because SRV requires a '_' to prefix it's test data
    def add_fqdn_argument(parser, required=True):
        parser.add_argument(
            '--fqdn', default="", type=str, dest='fqdn',
            help="The FQDN of the record being created. If you use this "
            "option you cannot use label or domain", required=required
        )

    def test_data():
        if rdtype == "CNAME":
            # Make the target different so avoid cname loop errors
            return 'fqdn', "A" + TEST_FQDN
        if rdtype == "SRV":
            return 'fqdn', "_" + TEST_FQDN
        else:
            return 'fqdn', TEST_FQDN

    return add_fqdn_argument, build_extractor(field_name, 'fqdn'), test_data


def system_argument(field_name):
    display_name = field_name.replace('_', '-')

    def add_system_argument(parser, required=True):
        parser.add_argument(
            '--{0}'.format(display_name), default="", type=str,
            dest=field_name, help="The hostname of the system this "
            "registration is associated with", required=True
        )

    def test_data():
        return 'system-hostname', 'toolsdev1.dmz.scl3.mozilla.com'

    extractor = build_extractor(field_name, field_name)
    return add_system_argument, extractor, test_data


def ip_argument(field_name, ip_type):
    def add_ip_argument(parser, required=True):
        parser.add_argument(
            '--ip', default=None, type=str, dest='ip',
            help="A string representation of an IP address.",
            required=required
        )

    def test_data():
        if ip_type == '4':
            return 'ip', TEST_IPv4()
        elif ip_type == '6':
            return 'ip', TEST_IPv6()

    return add_ip_argument, build_extractor(field_name, 'ip'), test_data


def target_argument(field_name):
    def add_target_arg(parser, required=True):
        parser.add_argument(
            '--target', default=None, type=str, dest='target',
            help="The target name of a record", required=required
        )

    def test_data():
        return 'target', TEST_FQDN

    return add_target_arg, build_extractor(field_name, 'target'), test_data


def name_argument(field_name, prefix='nic'):
    def add_com_arg(parser, required=False, **kwargs):
        parser.add_argument(
            '--{0}'.format('name'), type=str,
            dest='name', help="A short name",
            required=required
        )

    def test_data():
        return 'name', TEST_INAME(prefix=prefix)  # Reuse this test data

    return add_com_arg, build_extractor(field_name, 'name'), test_data


def text_argument(field_name):
    def add_text_argument(parser, required=True):
        parser.add_argument(
            '--text', default=None, type=str, dest='text',
            help="The text data.", required=required
        )

    def test_data():
        return 'text', TEST_TEXT

    return add_text_argument, build_extractor(field_name, 'text'), test_data


def ttl_argument(field_name):
    def add_ttl_argument(parser, **kwargs):
        write_num_argument(
            parser, 'ttl', 'ttl', "The ttl of a record.", required=False
        )

    def extract_ttl(nas):
        data = {}
        if nas.ttl:
            data['ttl'] = nas.ttl
        return data

    def test_data():
        return 'ttl', TEST_TTL

    return add_ttl_argument, build_extractor(field_name, 'ttl'), test_data


def key_argument(field_name):
    def add_key_argument(parser, required=True):
        parser.add_argument(
            '--key', default=None, type=str, dest='sshfp_key',
            help="The key data.", required=required
        )


def algorithm_argument(field_name):
    def add_algorithm_argument(parser, required=True):
        parser.add_argument(
            '--algo', metavar="algorithm type", type=str, dest='algorith_type',
            choices=['RSA', 'DSS'],
            help="The Algorithm type. See RFC 4255.", required=required
        )
        return parser


def fingerprint_argument(field_name):
    def add_fingerprint_argument(parser, required=False):
        parser.add_argument(
            '--finger-type', metavar="fingerprint number", type=str,
            dest='fingerprint_type', choices=['SHA1'], default='SHA1',
            help="The fingerprint type. See RFC 4255", required=required
        )
        return parser


def priority_argument(field_name):
    def add_priority_arg(parser, required=True):
        write_num_argument(
            parser, 'priority', 'priority', "The priority number of a record",
            required=required
        )

    def test_data():
        return 'priority', TEST_PRIORITY

    return add_priority_arg, build_extractor(field_name, 'priority'), test_data


def port_argument(field_name):
    def add_port_argument(parser, required=True):
        write_num_argument(
            parser, 'port', 'port', "The target port of an SRV " "record",
            required=required
        )

    def test_data():
        return 'port', TEST_PORT

    return add_port_argument, build_extractor(field_name, 'port'), test_data


def weight_argument(field_name):
    def add_weight_arg(parser, required=True):
        write_num_argument(
            parser, 'weight', 'weight', "The " "weight number of an SRV "
            "record", required=required
        )

    def test_data():
        return 'weight', TEST_WEIGHT

    return add_weight_arg, build_extractor(field_name, 'weight'), test_data
