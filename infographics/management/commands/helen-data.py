from django.core.management.base import BaseCommand
import urllib.request


class Command(BaseCommand):
    help = 'Parse and save example production data'

    def handle(self, *args, **options):
        self.run()
        self.stdout.write(self.style.SUCCESS('Successfully updated production data'))

    def run(self):
        url = 'https://www.helen.fi/sahko/kodit/aurinkosahko/suvilahti/DownloadData/'
        file, headers = urllib.request.urlretrieve(url)
        contents = open(file).read()
        splt = contents.splitlines()
        for i in range(20):
            print(i, ':', splt[i])



# temp_file = open('test.txt', 'w')








# with urllib.request.urlopen(url) as response:
#     contents = open(response[0]).read()
#     f = open('test.txt', 'w')
#     f.write(contents)
#     f.close()



# response = urllib.urlretrieve(url)
# contents = open(response[0]).read()
# f = open('filename.ext','w')
# f.write(contents)
# f.close()