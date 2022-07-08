from odoo import api, fields, models, _
from werkzeug import urls
from odoo.addons.http_routing.models.ir_http import url_for

class slideCustomChannel(models.Model):
    _inherit = 'slide.channel'
    preview_video = fields.Binary("Preview Video")
    preview_video_url = fields.Char("Preview URL")
    computed_url = fields.Char("Computed URL")

    @api.onchange("preview_video_url")
    def url_computation(self):
        if self:
            if self.preview_video_url:
                url_obj = urls.url_parse(self.preview_video_url)
                if url_obj.ascii_host == 'youtu.be':
                    return ('youtube', url_obj.path[1:] if url_obj.path else False)
                elif url_obj.ascii_host in (
                'youtube.com', 'www.youtube.com', 'm.youtube.com', 'www.youtube-nocookie.com'):
                    v_query_value = url_obj.decode_query().get('v')
                    if v_query_value:
                        self.write({
                            "computed_url": v_query_value,
                        })
                    else:
                        self.computed_url = False