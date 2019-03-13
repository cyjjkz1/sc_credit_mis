from ..models.school import Classify
from flask import jsonify
from base_handler import with_credit_user, BaseHandler
from app import db


class ProjectHandler(BaseHandler):
    def get(self):
        ret = self.handle()
        return jsonify(ret)

    @with_credit_user
    def _handle(self, *args, **kwargs):
        try:
            classify_all = Classify.query.all()
            temp_class = []
            if classify_all:
                for classify in classify_all:
                    temp_class.append(classify.to_dict())
            return temp_class
        except BaseException as e:
            db.session.rollback()
            raise e


