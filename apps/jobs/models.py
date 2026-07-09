from django.db import models
from django.conf import settings  # Use this for lazy model references
from django.utils import timezone
import uuid

# REMOVED: from django.contrib.auth import get_user_model
# REMOVED: User = get_user_model()

class Job(models.Model):
    # ... (Keep your Choices classes as they are)
    class JobType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        CONTRACT = 'contract', 'Contract'
        FREELANCE = 'freelance', 'Freelance'
        INTERNSHIP = 'internship', 'Internship'

    class WorkMode(models.TextChoices):
        ONSITE = 'onsite', 'On-site'
        REMOTE = 'remote', 'Remote'
        HYBRID = 'hybrid', 'Hybrid'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'entry', 'Entry Level'
        MID = 'mid', 'Mid Level'
        SENIOR = 'senior', 'Senior Level'
        LEAD = 'lead', 'Lead'
        EXECUTIVE = 'executive', 'Executive'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # CORRECTED: Use settings.AUTH_USER_MODEL
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posted_jobs'
    )
    
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    work_mode = models.CharField(max_length=20, choices=WorkMode.choices, default=WorkMode.ONSITE)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.MID)
    location = models.CharField(max_length=200, blank=True)
    is_remote_friendly = models.BooleanField(default=False)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    salary_period = models.CharField(max_length=20, default='year', choices=[('hour','Per Hour'),('day','Per Day'),('month','Per Month'),('year','Per Year')])
    skills_required = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    application_url = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    deadline = models.DateTimeField()
    view_count = models.PositiveIntegerField(default=0)
    application_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return timezone.now() > self.deadline

class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        REVIEWING = 'reviewing', 'Under Review'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        REJECTED = 'rejected', 'Rejected'
        HIRED = 'hired', 'Hired'

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    
    # CORRECTED: Use settings.AUTH_USER_MODEL
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='job_applications'
    )
    
    cover_letter = models.TextField()
    cv = models.FileField(upload_to='applications/cvs/', blank=True)
    portfolio_url = models.URLField(blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'applicant']