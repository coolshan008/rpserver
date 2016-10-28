from django.db import models

# Create your models here.

# CLASSROOM should be sync with the one in trainer


class CLASSROOM(models.Model):
    # Name=models.CharField(max_length=50)
    No = models.IntegerField()
    Name = models.CharField(max_length=20)
    Num_of_device = models.IntegerField()

    def __unicode__(self):
        return self.Name


class DEVICE(models.Model):
    Mac = models.CharField(max_length=40)
    # Ssi = models.IntegerField()
    # LastTime=models.DateTimeField('LastTime')
    Place = models.ForeignKey(CLASSROOM)
    Time_to_live = models.IntegerField()  # -1 to indicate that the device has not been classified

    def __unicode__(self):
        return self.Mac


class SIGNAL(models.Model):
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
    # Correct_no = models.IntegerField()1
    # Used = models.BooleanField()
    # Time = models.FloatField()

    def __unicode__(self):
        return self.Mac + '_' + self.Array + '_'
