from odoo import models, fields, api, _


class PublishedUnpublished(models.Model):
    _inherit = ['slide.slide']
    # s_id =

    def state_unpublished(self):
        self.is_published = False

    def state_published(self):
        self.is_published = True


