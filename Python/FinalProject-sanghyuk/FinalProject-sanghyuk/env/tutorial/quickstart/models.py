from django.db import models


class AA(models.Model):
    m_number = models.IntegerField(primary_key=True)
    m_name = models.CharField(max_length=45, blank=True, null=True)
    m_lcc = models.CharField(max_length=45, blank=True, null=True)
    m_lcn = models.CharField(max_length=45, blank=True, null=True)
    m_mcc = models.CharField(max_length=45, blank=True, null=True)
    m_mcn = models.CharField(max_length=45, blank=True, null=True)
    m_scc = models.CharField(max_length=45, blank=True, null=True)
    m_scn = models.CharField(max_length=45, blank=True, null=True)
    c_code = models.IntegerField(blank=True, null=True)
    c_name = models.CharField(max_length=45, blank=True, null=True)
    gg_code = models.IntegerField(blank=True, null=True)
    gg_name = models.CharField(max_length=45, blank=True, null=True)
    ad_name = models.CharField(max_length=45, blank=True, null=True)
    st_name = models.CharField(max_length=45, blank=True, null=True)
    stad_name = models.CharField(max_length=45, blank=True, null=True)
    o_mb = models.IntegerField(blank=True, null=True)
    n_mb = models.IntegerField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aa'


class Address(models.Model):
    ad_name = models.CharField(max_length=25, blank=True, null=True)
    st_name = models.CharField(max_length=22, blank=True, null=True)
    stad_name = models.CharField(max_length=29, blank=True, null=True)
    o_mb = models.CharField(max_length=7, blank=True, null=True)
    n_mb = models.CharField(max_length=5, blank=True, null=True)
    m_number = models.ForeignKey('Mall', models.DO_NOTHING, db_column='m_number', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'


class City(models.Model):
    c_code = models.CharField(primary_key=True, max_length=2)
    c_name = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'


class Ggun(models.Model):
    gg_code = models.CharField(primary_key=True, max_length=5)
    gg_name = models.CharField(max_length=5, blank=True, null=True)
    c_code = models.ForeignKey(City, models.DO_NOTHING, db_column='c_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ggun'


class Large(models.Model):
    m_lcc = models.CharField(primary_key=True, max_length=1)
    m_lcn = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'large'


class Lnglat(models.Model):
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    m_number = models.ForeignKey('Mall', models.DO_NOTHING, db_column='m_number', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lnglat'


class Mall(models.Model):
    m_number = models.CharField(primary_key=True, max_length=12)
    m_name = models.CharField(max_length=40, blank=True, null=True)
    gg_code = models.ForeignKey(Ggun, models.DO_NOTHING, db_column='gg_code', blank=True, null=True)
    m_scc = models.ForeignKey('Small', models.DO_NOTHING, db_column='m_scc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mall'


class Middle(models.Model):
    m_mcc = models.CharField(primary_key=True, max_length=3)
    m_mcn = models.CharField(max_length=15, blank=True, null=True)
    m_lcc = models.ForeignKey(Large, models.DO_NOTHING, db_column='m_lcc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'middle'


class PyboAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    question = models.ForeignKey('PyboQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pybo_answer'


class PyboQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pybo_question'


class Small(models.Model):
    m_scc = models.CharField(primary_key=True, max_length=6)
    m_scn = models.CharField(max_length=15, blank=True, null=True)
    m_mcc = models.ForeignKey(Middle, models.DO_NOTHING, db_column='m_mcc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'small'