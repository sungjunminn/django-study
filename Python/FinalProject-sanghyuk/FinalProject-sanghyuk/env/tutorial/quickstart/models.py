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




class Post(models.Model):
    table = models.CharField(max_length=30)
    m_lcc = models.CharField(max_length=30)
    m_mcc = models.CharField(max_length=30)
    m_scc = models.CharField(max_length=30)


class SeoulPplDong(models.Model):
    gu = models.TextField(blank=True, null=True)
    dong = models.TextField(blank=True, null=True)
    house = models.IntegerField(blank=True, null=True)
    all_sum = models.IntegerField(blank=True, null=True)
    male = models.IntegerField(blank=True, null=True)
    female = models.IntegerField(blank=True, null=True)
    korean = models.IntegerField(blank=True, null=True)
    k_male = models.IntegerField(blank=True, null=True)
    k_pemale = models.IntegerField(blank=True, null=True)
    fore = models.IntegerField(blank=True, null=True)
    f_male = models.IntegerField(blank=True, null=True)
    f_peemale = models.IntegerField(blank=True, null=True)
    ppl_house = models.IntegerField(blank=True, null=True)
    old = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul_ppl_dong'



class Chart(models.Model):
    si = models.CharField(max_length=30)
    gu = models.CharField(max_length=30)
    dong = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'quickstart_chart'