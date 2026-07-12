from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg
from django.views.generic import ListView
from apps.notifications.models import Notification

from django.views import View
from django.shortcuts import get_object_or_404, redirect
from apps.notifications.models import Notification

from apps.posts.models import Post
from apps.projects.models import Project
from apps.marketplace.models import Product
from apps.notifications.models import Notification
from apps.messaging.models import Message
from apps.reviews.models import Review
from apps.orders.models import Order
from apps.jobs.models import Job



class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard/dashboard.html"



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.request.user



        # ==========================
        # PROFILE
        # ==========================

        context["profile"] = getattr(
            user,
            "profile",
            None
        )



        # ==========================
        # STATS
        # ==========================


        context["projects_count"] = (
            Project.objects
            .filter(
                owner=user
            )
            .count()
        )



        context["products_count"] = (
            Product.objects
            .filter(
                owner=user
            )
            .count()
        )



        context["earnings"] = (
            Order.objects
            .filter(
                product__owner=user,
                status="completed"
            )
            .aggregate(
                total=Sum("amount")
            )
            ["total"] or 0
        )



        context["rating"] = (
            Review.objects
            .filter(
                developer=user
            )
            .aggregate(
                avg=Avg("rating")
            )
            ["avg"] or 0
        )



        # ==========================
        # COMMUNITY FEED
        # ==========================


        context["recent_posts"] = (
    Post.objects
    .filter(
        is_published=True
    )
    .select_related(
        "author",
        "author__profile"
    )
    .prefetch_related(
        "images"
    )
    .order_by(
        "-created_at"
    )[:3]
)




        # ==========================
        # MY PROJECTS
        # ==========================

        # ==========================
        # MY PROJECTS
        # ==========================

        context["projects"] = (
            Project.objects
            .filter(owner=user)
            .select_related(
                "owner",
                "owner__profile",
            )
            .order_by("-created_at")[:6]
        )

        # ==========================
        # MY PRODUCTS
        # ==========================

        context["products"] = (
            Product.objects
            .filter(owner=user)
            .order_by("-created_at")[:5]
        )


        # ==========================
        # SAVED JOBS
        # ==========================


        if hasattr(user, "saved_jobs"):

            context["saved_jobs"] = (
                user.saved_jobs
                .all()
                .order_by(
                    "-created_at"
                )[:5]
            )

        else:

            context["saved_jobs"] = []





        # ==========================
        # NOTIFICATIONS
        # ==========================


        context["notifications"] = (
            Notification.objects
            .filter(
                user=user
            )
            .order_by(
                "-created_at"
            )[:6]
        )





        # ==========================
        # MESSAGES
        # ==========================


        context["messages"] = (
            Message.objects
            .filter(
                receiver=user
            )
            .select_related(
                "sender"
            )
            .order_by(
                "-created_at"
            )[:5]
        )





        # ==========================
        # REVIEWS
        # ==========================


        context["reviews"] = (
            Review.objects
            .filter(
                developer=user
            )
            .select_related(
                "reviewer"
            )
            .order_by(
                "-created_at"
            )[:5]
        )





        # ==========================
        # COMMUNITY STATS
        # ==========================


        context["community_stats"] = {

            "developers":
                user.__class__.objects.count(),


            "projects":
                Project.objects.count(),


            "posts":
                Post.objects.count(),


            "jobs":
                Job.objects.count(),

        }



        return context
    
    



class NotificationsView(LoginRequiredMixin, ListView):

    model = Notification

    template_name = "dashboard/notifications.html"

    context_object_name = "notifications"


    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        ).order_by(
            "-created_at"
        )

class MarkNotificationReadView(LoginRequiredMixin, View):

    def post(self, request, pk):

        notification = get_object_or_404(
            Notification,
            id=pk,
            user=request.user
        )

        notification.is_read = True
        notification.save()

        return redirect("dashboard:index")