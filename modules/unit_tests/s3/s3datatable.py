# -*- coding: utf-8 -*-
#
# S3Resource Unit Tests
#
# To run this script use:
# python web2py.py -S eden -M -R applications/eden/modules/unit_tests/s3/s3datatable.py
#
import unittest
import datetime
from gluon import *
from gluon.storage import Storage
from gluon.dal import Row

from s3.s3utils import S3DataTable

# =============================================================================
class S3DataTableTests(unittest.TestCase):

    def get_display_fields(self,
                           list_fields,
                           **attr
                           ):
        """
            Method to return the list of fields that will be displayed

            @param list_fields: list of field selectors
            @param attr: dictionary of attributes which can be passed in
                   no_ids: Don't include the row ids in the result
        """

        s3db = current.s3db
        resource = self.resource
        row = Storage()
        fieldlist = []

        table = resource.table
        if table._id.name not in list_fields:
            list_fields.insert(0, table._id.name)
        ffields = resource.rfilter.get_fields()
        for f in ffields:
            if f not in list_fields:
                list_fields.append(f)
        lfields, joins, ljoins, d = resource.resolve_selectors(list_fields)
        # Get the labels from the Fields
        for s3field in lfields:
            if s3field.field:
                name = str(s3field.field)
            else:
                if s3field.virtual:
                    name = None
                    vlist = s3db[s3field.tname].virtualfields
                    for vf in vlist:
                        if s3field.fname in dir(vf):
                            # it's a virtual field
                            name = "%s.%s" % (s3field.tname, s3field.fname)
                            break
            if not name:
                # Invalid field
                continue
            fieldlist.append(name)
            row[name] = s3field.label
        return (fieldlist, row)

    def setUp(self):
        """
            Set up the list of fields each time since the call to S3DataTables
            could change it.
        """
        self.resource = current.manager.define_resource("org", "office")
        list_fields = ["id",
                       "name",
                       "organisation_id$name",
                       "organisation_id$address",
                       "office_type_id",
                       "location_id$L0",
                       "location_id$L1",
                       "location_id$L2",
                       "location_id$L3",
                       "phone1",
                       "email"
                       ]
        rows = self.resource._select(list_fields)
        self.data = self.resource._extract(rows, list_fields)
        self.lfields, self.row = self.get_display_fields(list_fields)



    def testSqlTableHTML(self):
        """
            render to an HTML TABLE
        """
        dt = S3DataTable(self.data, self.lfields, self.row)
        actual = dt.html()
        # @todo: Need to add a test for the format returned
        print actual
        dt = S3DataTable(self.data, self.lfields, self.row, start = 3, limit = 5)
        actual = dt.html()
        # @todo: Need to add a test for the format returned
        print actual


    def testSqlTableJSON(self):
        """
            render to a JSON Object
        """
        dt = S3DataTable(self.data, self.lfields, self.row)
        actual = dt.json("list_1", 1, 14, 14)
        # @todo: Need to add a test for the format returned
        print actual
        dt = S3DataTable(self.data, self.lfields, self.row, start = 3, limit = 5)
        actual = dt.json("list_1", 1, 14, 14)
        # @todo: Need to add a test for the format returned
        print actual

    def tearDown(cls):
        pass

# =============================================================================
def run_suite(*test_classes):
    """ Run the test suite """

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    if suite is not None:
        unittest.TextTestRunner(verbosity=2).run(suite)
    return

if __name__ == "__main__":

    run_suite(
        S3DataTableTests,
    )

# END ========================================================================