from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Delivery


@login_required
def delivery_dashboard(request):
    if not hasattr(request.user, 'profile'):
        return render(
            request,
            'delivery/access_denied.html',
            {
                'message': 'Delivery profile not found.'
            }
        )

    if request.user.profile.role != 'delivery':
        return render(
            request,
            'delivery/access_denied.html',
            {
                'message': 'You are not authorized to access the delivery dashboard.'
            }
        )

    deliveries = Delivery.objects.filter(
        delivery_person=request.user
    ).select_related(
        'order',
        'order__customer'
    ).order_by('-updated_at')

    return render(
        request,
        'delivery/dashboard.html',
        {
            'deliveries': deliveries
        }
    )
