This is a demo project that shows how to deal with circular dependencies when
squashing Django migrations.

The project has two apps: `fruit` and `meat`. An `Apple` has many `Bacon`
children, and a `Bacon` has many `Cranberry` children. You can see that the
fruit app depends on the meat app, and the meat app depends on the fruit app.

The first commit creates all three models with a name field on each and
foreign keys from `Cranberry` to `Bacon` and from `Bacon` to `Apple`. Calling
`makemigrations` creates three migrations:
* `fruit/0001_initial` creates the `Apple` and `Cranberry` models
* `meat/0001_initial` creates the `Bacon` model with its foreign key to `Apple`
* `fruit/0002_cranberry_bacon` adds the foreign key from `Cranberry` to `Bacon`

The next commit adds an `Apple.size` field just so there is something to squash.
Calling `makemigrations` adds another migration:
* `fruit/0003_apple_size` adds the `size` field

Now it's time to squash migrations. Running `squashmigrations` now would create
a squashed migration with a circular dependency, so we replace the foreign key
from `Cranberry` to `Bacon` with an integer field. Override the field name so it
has the `_id` suffix of a foreign key.

    # TODO: switch back to the foreign key.
    # bacon = models.ForeignKey('meat.Bacon', null=True)
    bacon = models.IntegerField(db_column='bacon_id', null=True)

Run `makemigrations` and rename the migration to show that it is starting
the squash process:
* `fruit/0100_unlink_apps` converts the foreign key to an integer field

Now run `squashmigrations fruit 0100` and rename the migration to make it easier
to follow the sequence:
* `fruit/0101_squashed` combines all the migrations from 1 to 100.

Comment out the dependency from `fruit/0101_squashed` to `meat/0001_initial`. It
isn't really needed, and it creates a circular dependency. With more complicated
migration histories, the foreign keys to other apps might not get optimized out.
Search the file for all the app names listed in the dependencies to see if there
are any foreign keys left. If so, manually replace them with the integer fields.
Usually, this means replacing a `CreateModel(...ForeignKey...)` and
`AlterModel(...IntegerField...)` with a `CreateModel(...IntegerField...)`.

The next commit contains all these changes for demonstration purposes. It
wouldn't make sense to push it without the following commit, though, because
the apps are still unlinked.

Switch back to the foreign key from `Cranberry` to `Bacon`, and run
`makemigrations` one last time. Rename the migration to show that it is
finishing the squash process:
* `fruit/0102_relink_apps` converts the integer field back to a foreign key

Remove the dependency from `fruit/0102_relink_apps` to `fruit/0101_squashed`,
and add a dependency from `fruit/0102_relink_apps` to `fruit/0100_unlink_apps`.
The original dependency just won't work. Take the dependencies that were
commented out in `fruit/0101_squashed` and add them to `fruit/0102_relink_apps`.
That will ensure the links get created in the right order.

Run the test suite to show that the squashed migration works properly. If you
can, test against something other than SQLite, because it doesn't catch some
foreign key problems. Running in verbose mode will list all the migrations as
they run. Back up the development or production database and run `migrate` to
see that the unlinking and relinking of the apps doesn't break anything.

Take a nap.

## Bonus section: after all installations are squashed ##
The `remove_replaced` branch shows what could happen in the future once all
installations have migrated past the squash point. Delete all the migrations
from 1 to 100, because they've been replaced by 101. Delete the `replaces` list
from `fruit/0101_squashed`. Run `showmigrations` to check for any broken
dependencies, and replace them with `fruit/0101_squashed`. 
