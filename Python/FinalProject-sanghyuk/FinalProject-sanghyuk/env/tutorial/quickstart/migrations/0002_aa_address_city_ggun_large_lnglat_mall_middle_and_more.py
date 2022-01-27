# Generated by Django 4.0.1 on 2022-01-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AA',
            fields=[
                ('m_number', models.IntegerField(primary_key=True, serialize=False)),
                ('m_name', models.CharField(blank=True, max_length=45, null=True)),
                ('m_lcc', models.CharField(blank=True, max_length=45, null=True)),
                ('m_lcn', models.CharField(blank=True, max_length=45, null=True)),
                ('m_mcc', models.CharField(blank=True, max_length=45, null=True)),
                ('m_mcn', models.CharField(blank=True, max_length=45, null=True)),
                ('m_scc', models.CharField(blank=True, max_length=45, null=True)),
                ('m_scn', models.CharField(blank=True, max_length=45, null=True)),
                ('c_code', models.IntegerField(blank=True, null=True)),
                ('c_name', models.CharField(blank=True, max_length=45, null=True)),
                ('gg_code', models.IntegerField(blank=True, null=True)),
                ('gg_name', models.CharField(blank=True, max_length=45, null=True)),
                ('ad_name', models.CharField(blank=True, max_length=45, null=True)),
                ('st_name', models.CharField(blank=True, max_length=45, null=True)),
                ('stad_name', models.CharField(blank=True, max_length=45, null=True)),
                ('o_mb', models.IntegerField(blank=True, null=True)),
                ('n_mb', models.IntegerField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'aa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_name', models.CharField(blank=True, max_length=25, null=True)),
                ('st_name', models.CharField(blank=True, max_length=22, null=True)),
                ('stad_name', models.CharField(blank=True, max_length=29, null=True)),
                ('o_mb', models.CharField(blank=True, max_length=7, null=True)),
                ('n_mb', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'address',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('c_code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('c_name', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ggun',
            fields=[
                ('gg_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('gg_name', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'ggun',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Large',
            fields=[
                ('m_lcc', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('m_lcn', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'large',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lnglat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lng', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lnglat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mall',
            fields=[
                ('m_number', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('m_name', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'mall',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Middle',
            fields=[
                ('m_mcc', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('m_mcn', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'middle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PyboAnswer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'pybo_answer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PyboQuestion',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'pybo_question',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Small',
            fields=[
                ('m_scc', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('m_scn', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'small',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]