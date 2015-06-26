from pbtests.packetbeat import TestCase


class Test(TestCase):
    """
    Basic MongoDB tests
    """

    def test_mongodb_use_db(self):
        """
        Should correctly pass a MongoDB database access query
        """
        self.render_config_template(
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongodb_use_db.pcap",
                            debug_selectors=["mongodb", "sniffer"])

        objs = self.read_output()
        o = objs[0]
        assert o["type"] == "mongodb"

    def test_mongodb_create_collection(self):
        """
        Should correctly pass a create collection MongoDB database query
        """
        self.render_config_template(
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongodb_create_collection.pcap",
                            debug_selectors=["mongodb"])

        objs = self.read_output()
        o = objs[0]
        assert o["type"] == "mongodb"

    def test_mongodb_find(self):
        """
        Should correctly pass a simple MongoDB find query
        """
        self.render_config_template(
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongodb_find.pcap",
                            debug_selectors=["mongodb"])

        objs = self.read_output()
        o = objs[0]
        assert o["type"] == "mongodb"
        assert o["method"] == "find"
        assert o["status"] == "OK"

    def test_mongodb_find_one(self):
        """
        Should correctly pass a simple MongoDB find query.
        The request and response fields should not be in
        by default.
        """
        self.render_config_template(
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongo_one_row.pcap",
                            debug_selectors=["mongodb"])

        objs = self.read_output()
        o = objs[0]
        assert o["type"] == "mongodb"
        assert o["method"] == "find"
        assert "request" not in o
        assert "response" not in o

    def test_mongodb_send_response(self):
        """
        Should put the request and the response fields in
        when requested.
        """
        self.render_config_template(
            mongodb_send_request=True,
            mongodb_send_response=True,
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongo_one_row.pcap",
                            debug_selectors=["mongodb"])

        objs = self.read_output()
        assert len(objs) == 1
        o = objs[0]
        assert "request" in o
        assert "response" in o
        assert len(o["response"].splitlines()) == 1

    def test_mongodb_send_response_more_rows(self):
        """
        Should work when the query is returning multiple
        documents.
        """
        self.render_config_template(
            mongodb_send_request=True,
            mongodb_send_response=True,
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongodb_more_rows.pcap",
                            debug_selectors=["mongodb"])

        objs = self.read_output()
        assert len(objs) == 1
        o = objs[0]
        assert "request" in o
        assert "response" in o
        assert len(o["response"].splitlines()) == 101

    def test_mongodb_inserts(self):
        """
        Should correctly pass a MongoDB insert command
        """
        self.render_config_template(
            mongodb_ports=[27017]
        )
        self.run_packetbeat(pcap="mongodb_inserts.pcap",
                            debug_selectors=["mongodb"])

        objs = self.read_output()
        o = objs[1]
        assert o["type"] == "mongodb"
        assert o["method"] == "insert"
