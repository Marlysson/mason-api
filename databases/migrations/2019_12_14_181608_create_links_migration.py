from orator.migrations import Migration


class CreateLinksMigration(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('Links') as table:
            table.increments('id')
            table.string('alias')
            table.string('redirect_to')
            table.integer('total_access')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('Links')
