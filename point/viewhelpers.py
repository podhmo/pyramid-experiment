class RegisterPredicate(object):
    @classmethod
    def confirm_p(context, request):
        return "confirm" == request.POST.get("stage")

    @classmethod
    def execute_p(context, request):
        return "execute" == request.POST.get("stage")
