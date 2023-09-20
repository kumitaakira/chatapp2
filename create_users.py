import os
import random

import django
from dateutil import tz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Message
from django.contrib.auth.models import User

fakegen = Faker(["ja_JP"])

def create_users(n):
    """
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    """

    users = [
        User(username=fakegen.user_name(), email=fakegen.ascii_safe_email())
        for _ in range(n)
    ]

    User.objects.bulk_create(users, ignore_conflicts=True)

    my_id = User.objects.get(username="kumitaakira").id    #type:ignore

    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    user_ids = User.objects.exclude(id=my_id).values_list("id", flat=True)

    talks = []
    for _ in range(len(user_ids)):
        sent_talk = Message(
            sender_id=my_id,
            to_user_id=random.choice(user_ids),
            content=fakegen.text(),
        )
        received_talk = Message(
            sender_id=random.choice(user_ids),
            to_user_id=my_id,
            content=fakegen.text(),
        )
        talks.extend([sent_talk, received_talk])
    Message.objects.bulk_create(talks, ignore_conflicts=True)

    # Talk の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    talks = Message.objects.order_by("-pub_date")[: 2 * len(user_ids)]
    for talk in talks:
        talk.pub_date = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Message.objects.bulk_update(talks, fields=["pub_date"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(4)
    print("done")