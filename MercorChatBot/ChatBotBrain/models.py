# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid


class Education(models.Model):
    educationId = models.CharField(db_column='educationId', primary_key=True, max_length=255)
    degree = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    startDate = models.CharField(db_column='startDate', max_length=255, blank=True, null=True)
    endDate = models.CharField(db_column='endDate', max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)
    resumeId = models.ForeignKey('UserResume', models.DO_NOTHING, db_column='resumeId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Education'


class MercorUserSkills(models.Model):
    userId = models.OneToOneField('MercorUsers', models.DO_NOTHING, db_column='userId', primary_key=True)
    skillId = models.ForeignKey('Skills', models.DO_NOTHING, db_column='skillId')
    isPrimary = models.IntegerField(db_column='isPrimary')
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'MercorUserSkills'
        unique_together = (('userId', 'skillId'),)


class MercorUsers(models.Model):
    userid = models.CharField(db_column='userId', primary_key=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    residence = models.JSONField(blank=True, null=True)
    profilePic = models.TextField(db_column='profilePic', blank=True, null=True)
    createdAt = models.DateTimeField(db_column='createdAt')
    lastLogin = models.DateTimeField(db_column='lastLogin')
    notes = models.TextField(blank=True, null=True)
    referralCode = models.CharField(db_column='referralCode', unique=True, max_length=255, blank=True, null=True)
    isGptEnabled = models.IntegerField(db_column='isGptEnabled')
    preferredRole = models.CharField(db_column='preferredRole', max_length=255, blank=True, null=True)
    fullTimeStatus = models.CharField(db_column='fullTimeStatus', max_length=255, blank=True, null=True)
    workAvailability = models.CharField(db_column='workAvailability', max_length=255, blank=True, null=True)
    fullTimeSalaryCurrency = models.CharField(db_column='fullTimeSalaryCurrency', max_length=255, blank=True, null=True)
    fullTimeSalary = models.CharField(db_column='fullTimeSalary', max_length=255, blank=True, null=True)
    partTimeSalaryCurrency = models.CharField(db_column='partTimeSalaryCurrency', max_length=255, blank=True, null=True)
    partTimeSalary = models.CharField(db_column='partTimeSalary', max_length=255, blank=True, null=True)
    fullTime = models.IntegerField(db_column='fullTime')
    fullTimeAvailability = models.IntegerField(db_column='fullTimeAvailability', blank=True, null=True)
    partTime = models.IntegerField(db_column='partTime')
    partTimeAvailability = models.IntegerField(db_column='partTimeAvailability', blank=True, null=True)
    w8BenUrl = models.JSONField(db_column='w8BenUrl', blank=True, null=True)
    tosUrl = models.TextField(db_column='tosUrl', blank=True, null=True)
    policyUrls = models.JSONField(db_column='policyUrls', blank=True, null=True)
    isPreVetted = models.IntegerField(db_column='isPreVetted')
    isActive = models.IntegerField(db_column='isActive')
    isComplete = models.IntegerField(db_column='isComplete')
    summary = models.TextField(blank=True, null=True)
    preVettedAt = models.DateTimeField(db_column='preVettedAt', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MercorUsers'


class PersonalInformation(models.Model):
    personalInformationId = models.CharField(db_column='personalInformationId', primary_key=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    location = models.JSONField(blank=True, null=True)
    email = models.JSONField(blank=True, null=True)
    phone = models.JSONField(blank=True, null=True)
    resumeId = models.ForeignKey('UserResume', models.DO_NOTHING, db_column='resumeId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PersonalInformation'


class Skills(models.Model):
    skillId = models.CharField(db_column='skillId', primary_key=True, max_length=255)
    skillName = models.CharField(db_column='skillName', max_length=255)
    skillValue = models.CharField(db_column='skillValue', unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'Skills'


class UserResume(models.Model):
    resumeId = models.CharField(db_column='resumeId', primary_key=True, max_length=255)
    url = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=255)
    createdAt = models.DateTimeField(db_column='createdAt')
    updatedAt = models.DateTimeField(db_column='updatedAt')
    source = models.CharField(max_length=255)
    ocrText = models.TextField(db_column='ocrText', blank=True, null=True)
    ocrEmail = models.CharField(db_column='ocrEmail', max_length=255, blank=True, null=True)
    ocrGithubUsername = models.CharField(db_column='ocrGithubUsername', max_length=255, blank=True, null=True)
    resumeBasedQuestions = models.TextField(db_column='resumeBasedQuestions', blank=True, null=True)
    userId = models.OneToOneField(MercorUsers, models.DO_NOTHING, db_column='userId', blank=True, null=True)
    isInvitedToInterview = models.IntegerField(db_column='isInvitedToInterview')
    reminderTasksIds = models.JSONField(db_column='reminderTasksIds', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserResume'


class WorkExperience(models.Model):
    workExperienceId = models.CharField(db_column='workExperienceId', primary_key=True, max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    startDate = models.CharField(db_column='startDate', max_length=255, blank=True, null=True)
    endDate = models.CharField(db_column='endDate', max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    locationCity = models.CharField(db_column='locationCity', max_length=255, blank=True, null=True)
    locationCountry = models.CharField(db_column='locationCountry', max_length=255, blank=True, null=True)
    resumeId = models.ForeignKey(UserResume, models.DO_NOTHING, db_column='resumeId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WorkExperience'


class MercorUserProfile(models.Model):
    userid = models.CharField(db_column='userId', max_length=255, primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fullTimeSalary = models.CharField(db_column='fullTimeSalary', max_length=255, blank=True, null=True)
    partTimeSalary = models.CharField(db_column='partTimeSalary', max_length=255, blank=True, null=True)
    workExperience = models.JSONField(db_column='workExperience', blank=True, null=True)  # Field name made lowercase.
    education = models.JSONField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MercorUserProfile'


class Chat(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    messages = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
