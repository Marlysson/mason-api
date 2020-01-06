from orator.migrations import Migration


class CreateLinksMigration(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('Links') as table:
            table.increments('id')
            table.string('alias')
            table.string('website')
            table.integer('total_access').default(0)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('Links')
