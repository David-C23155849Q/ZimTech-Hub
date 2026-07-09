from django.shortcuts import render

def job_list(request):
    """
    View to list all jobs.
    """
    # For now, this just renders a template named 'jobs/job_list.html'
    return render(request, 'jobs/job_list.html', {})