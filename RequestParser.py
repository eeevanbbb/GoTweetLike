class RequestParser(object):
    invalid_response = { "type" : "invalid", "message" : "Sorry, I couldn't understand that request. Tweet \"@GoTweetLike @Username\" to summon me!" }
    help_response = { "type" : "help", "message" : "I'm a bot that tweets like people! Tweet \"@GoTweetLike @Username\" to see me go!" }


    def get_at_list(self, request):
        ats = []
        words = request.split()
        for word in words:
            if word[0] == "@":
                ats.append(word)
            else:
                break
        return ats

    def parse_request(self, request):
        words = request.split()
        if len(words) < 2:
            return self.invalid_response
        else:
            at_list = self.get_at_list(request)
            if len(at_list) == 0:
                return self.invalid_response

            if at_list[0].lower() != '@gotweetlike':
                return self.invalid_response        

            if len(at_list) == 1:
                if words[1].lower() == 'help':
                    return self.help_response
                else:
                    return self.invalid_response
            elif len(at_list) == 2:
                if len(words) >= 3 and words[2].lower() == 'update':
                    return { 'type' : 'update', 'screen_name' : at_list[1] }
                else:
                    return { 'type' : 'standard', 'screen_name' : at_list[1] }
            else:
                return { 'type' : 'combined', 'screen_names' : at_list[1:] }

