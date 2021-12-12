# -*- coding: utf-8 -*-
 
# Importing Scrapy Library
import scrapy

# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
     
    # Spider name
    name = 'amazon_reviews'
     
    # Domain names to scrape
    allowed_domains = ['amazon.in']

    productIds = ['B000FNFL0G']
     
    # Base URL for the World Tech Toys Elite Mini Orion Spy Drone
    start_urls=[]
    #         myBaseUrl = "https://www.amazon.com/product-reviews/B000FNFL0G/ref=cm_cr_arp_d_viewopt_sr?pageNumber="

    # Creating list of urls to be scraped by appending page number a the end of base url
    for productId in productIds:
        myBaseUrl = "https://www.amazon.com/product-reviews/"+productId+"/ref=cm_cr_arp_d_viewopt_sr?pageNumber="
        for i in range(1,9):    
            start_urls.append(myBaseUrl+str(i))
    
    # Defining a Scrapy parser
    def parse(self, response):
            # Get the product info
            product_data = response.css('#cm_cr-product_info')
            print('product_data',product_data)

            product_info = product_data.css('.product-info')
            print("product_info",product_info)

             # Get product name
            product_name = product_info.css('.product-title').xpath(".//text()").extract()
            print('product_name',product_name)

            # Get brand name
            brand_name = product_info.css('.product-by-line').xpath(".//text()").extract()
            print('brand_name',brand_name)

            #Get the Review List
            data = response.css('#cm_cr-review_list')

            # Get a product by
            # brand_name = product_data.css('.cr-product-byline')

            # print('daproduct_infota',product_info)

            # print('brand_name',brand_name)

            #Get the Name
            name = data.css('.a-profile-name')
            print('name',name)
            #Get the Review Title
            title = data.css('.review-title')
            
            # Get the Ratings
            star_rating = data.css('.review-rating')
            
            # Get the users Comments
            comments = data.css('.review-text')
            comment_upvote = data.css('.cr-vote-text')
            dates = data.css('.review-date').xpath(".//text()").extract()
            new_date_array = []
            for date in dates:
                date_split = date.split()
                new_date = date_split[-3]+' '+date_split[-2]+date_split[-1]
                print("new_date",new_date)
                new_date_array.append(new_date)
            print("new_date_array",new_date_array)
            count = 0
            # combining the results
            for review in star_rating:
                yield{'Product Name':''.join(product_name),
                      'Brand':''.join(brand_name),
                      'Name':''.join(name[count].xpath(".//text()").extract()),
                      'Title':''.join(title[count].xpath(".//text()").extract()),
                      'Rating': ''.join(review.xpath('.//text()').extract()),
                      'Comment': ''.join(comments[count].xpath(".//text()").extract()),
                      'Helpful Vote' : ''.join(comment_upvote[count].xpath(".//text()").extract()),
                      'Date': ''.join(new_date_array[count])
                    }
                count=count+1