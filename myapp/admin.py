from django.contrib import admin

from myapp.models import *

from movies.models import *

admin.site.register(FollowingModel)

# admin.site.register(WishlistItems)

# admin.site.register(WatchlistItems)

admin.site.register(CustomUserModel)

# admin.site.register(ReviewItems)

