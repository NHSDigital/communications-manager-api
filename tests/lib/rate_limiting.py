import json
import time


class RateLimiting:
    def __init__(self, products_api, developer_apps_api, api_product_name, delay):
        self.products_api = products_api
        self.developer_apps_api = developer_apps_api
        self.api_product_name = api_product_name
        self.product = products_api.get_product_by_name(api_product_name)
        self.previous_ratelimit = self.extract_ratelimiting_attribute()
        self.delay = delay

    def extract_ratelimiting_attribute(self):
        if self.product["attributes"] is None:
            raise ValueError(f'Product "{self.api_product_name}" does not have any attributes')

        ratelimit = None
        for attribute in self.product["attributes"]:
            if attribute["name"] == 'ratelimiting':
                ratelimit = attribute["value"]
                break

        if ratelimit is None:
            raise ValueError(f'Product "{self.api_product_name}" does not have a ratelimit attribute')

        return ratelimit

    def restore_rate_limit(self):
        self.update_product_rate_limit(self.previous_ratelimit)

    def update_product_rate_limit(self, ratelimit):
        for attribute in self.product["attributes"]:
            if attribute["name"] == 'ratelimiting':
                attribute["value"] = ratelimit
                break

        self.products_api.put_product_by_name(self.api_product_name, self.product)
        time.sleep(self.delay)

    def set_default_rate_limit(self):
        self.set_rate_limit()

    def set_rate_limit(self, app_quota=1200, app_spikearrest="6000pm", proxy_quota=3600, proxy_spikearrest="18000pm"):
        config_dict = {
            "app": {
                "quota": {
                    "enabled": True,
                    "interval": 1,
                    "limit": app_quota,
                    "timeunit": "minute"
                },
                "spikeArrest": {
                    "enabled": True,
                    "ratelimit": app_spikearrest
                }
            },
            self.api_product_name: {
                "quota": {
                    "enabled": True,
                    "interval": 1,
                    "limit": proxy_quota,
                    "timeunit": "minute"
                },
                "spikeArrest": {
                    "enabled": True,
                    "ratelimit": proxy_spikearrest
                }
            }
        }
        ratelimit_value = json.dumps(config_dict)
        self.update_product_rate_limit(ratelimit_value)

    def remove_app_ratelimit(self, email, app_name):
        app = self.developer_apps_api.get_app_by_name(email, app_name)

        new_attributes = []

        for attribute in app["attributes"]:
            if attribute["name"] != 'ratelimiting':
                new_attributes.append(attribute)

        app["attributes"] = new_attributes

        self.developer_apps_api.put_app_by_name(email, app_name, app)

    def set_app_ratelimit(self, email, app_name, quota=1200, spikearrest="6000pm"):
        app = self.developer_apps_api.get_app_by_name(email, app_name)

        config_dict = {
            self.api_product_name: {
                "quota": {
                    "enabled": True,
                    "interval": 1,
                    "limit": quota,
                    "timeunit": "minute"
                },
                "spikeArrest": {
                    "enabled": True,
                    "ratelimit": spikearrest
                }
            }
        }

        ratelimit_value = json.dumps(config_dict)

        updated = False
        for attribute in app["attributes"]:
            if attribute["name"] == 'ratelimiting':
                attribute["value"] = ratelimit_value
                updated = True
                break

        if updated is False:
            app["attributes"].append({
                "name": "ratelimiting",
                "value": ratelimit_value
            })

        self.developer_apps_api.put_app_by_name(email, app_name, app)
