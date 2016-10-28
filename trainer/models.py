from django.db import models

# Create your models here.


class CLASSROOM(models.Model):
    # No = models.CharField(max_length=10)
    No = models.IntegerField()

    def __unicode__(self):
        return str(self.No)


class POSITION(models.Model):  # for android
    Mac = models.CharField(max_length=40)
    Time = models.FloatField()
    # No = models.CharField(max_length=10)  # correspond to CLASSROOM.No,refer to the actual position
    No = models.IntegerField()
    Used = models.BooleanField()

    def __unicode__(self):
        temp = "%f" % self.Time
        return self.Mac + '_' + temp + '_' + str(self.No) + '_' + str(self.Used)


class DEVICE(models.Model):
    Mac = models.CharField(max_length=40)
    Ssi = models.IntegerField()
    Time = models.FloatField()
    Class_No = models.IntegerField()  # pi's position

    def __unicode__(self):  # return Mac_Time
        temp = "%f" % self.Time
        return self.Mac + '_' + temp + '_' + str(self.Class_No)


class TUPLE(models.Model):
    Mac = models.CharField(max_length=40)
    Array = models.CharField(max_length=1000)
    Correct_no = models.IntegerField()
    Used = models.BooleanField()
    Time = models.FloatField()

    def __unicode__(self):
        return self.Mac + '_' + self.Array + '_'
