from rest_framework.response import Response


class MetaDataResponse(Response):
    meta_data_dict = {"meta": "", "result": "error", "data": {}}

    def __init__(self, *args, **kwargs):
        if args:
            if args[0].get("result"):
                MetaDataResponse.meta_data_dict["result"] = args[0]["result"]
                del args[0]["result"]
            MetaDataResponse.meta_data_dict["data"] = args[0]
            if len(args) >= 2:
                MetaDataResponse.meta_data_dict["meta"] = args[1]
            modified_args = tuple([MetaDataResponse.meta_data_dict])
        super(MetaDataResponse, self).__init__(*modified_args, **kwargs)
