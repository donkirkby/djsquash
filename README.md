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
a squashed migration with a circular dependency, so we try this horribly
complicated procedure:

1. Remove all of the migrations.

        $ rm fruit/migrations/0*
        $ rm meat/migrations/0*

2. Create a new set of migrations. This is the only way that I've seen Django
    properly break dependency cycles by separating `0001_initial` and
    `0002_cranberry_bacon`.

        $ ./manage.py makemigrations 
        Migrations for 'fruit':
          fruit/migrations/0001_initial.py
            - Create model Apple
            - Create model Cranberry
          fruit/migrations/0002_cranberry_bacon.py
            - Add field bacon to cranberry
        Migrations for 'meat':
          meat/migrations/0001_initial.py
            - Create model Bacon

3. Rename the new migrations to be replacements, and restore the old migrations.

        $ mv fruit/migrations/0001_initial.py fruit/migrations/0101_squashed.py
        $ mv fruit/migrations/0002_cranberry_bacon.py fruit/migrations/0102_link_apps.py
        $ git checkout -- .

4. Change the new migrations to actually be replacements for the old
    migrations. Look through the old migrations to see which ones depend on the
    other app. List those migrations in `0102_link_apps.py`, and list all the
    other migrations in `0101_squashed.py`.

        # Added to 0101_squashed.py
        replaces = [(b'fruit', '0001_initial'), (b'fruit', '0003_apple_size')]

        # Added to 0102_link_apps.py
        replaces = [(b'fruit', '0002_cranberry_bacon')]

5. Now comes the painful part on a large project. All of the old migrations
    that depend on the other app have to be taken out of the dependency chain.
    In my example, `0003_apple_size` now depends on `0001_initial` instead of
    `0002_cranberry_bacon`. Of course, Django gets upset if you have more than
    one leaf node in an app's migrations, so you need to link the two
    dependency chains back together at the end. Here's
    `fruit/migrations/0100_prepare_squash.py`:

        from __future__ import unicode_literals
        
        from django.db import migrations
        
        
        class Migration(migrations.Migration):
        
            dependencies = [
                ('fruit', '0003_apple_size'),
                ('fruit', '0002_cranberry_bacon'),
            ]
        
            operations = [
            ]

6. Add `0100_prepare_squash` to the list of migrations that `0102_link_apps`
    replaces.

        # Added to 0102_link_apps.py
        replaces = [(b'fruit', '0002_cranberry_bacon'), (b'fruit', '0100_prepare_squash')]

This seems horribly dangerous, particularly making changes to the dependencies
of the old migrations. I guess you could make the dependency chain more
elaborate to ensure that everything runs in the correct order, but that would
be even more painful to set up.

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
