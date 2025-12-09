
import unittest
from unittest.mock import patch, MagicMock
import json
import server

class TestFlexOffersPromotions(unittest.TestCase):
    
    @patch('server.requests.get')
    def test_get_flexoffers_promotions_success(self, mock_get):
        # Mock XML response
        mock_xml = """<?xml version="1.0" encoding="utf-8"?>
  <PaginatedResultSetOfLinkDto xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Results>
      <LinkDto>
        <AdvertiserId>168490</AdvertiserId>
        <AdvertiserName>NIKE</AdvertiserName>
        <LinkId>2.4942550.14487458</LinkId>
        <LinkType>Text Link</LinkType>
        <LinkName>Men's Shoe Nike Blazer Mid '77 Vintage, Shop Nike.com</LinkName>
        <LinkDescription>Men's Shoe Nike Blazer Mid '77 Vintage, Shop Nike.com</LinkDescription>
        <PromotionalTypes>General Promotion</PromotionalTypes>
        <LinkUrl>https://track.flexlinkspro.com/g.ashx?foid=2.4942550.14487458&amp;trid=177.168490&amp;foc=12&amp;fot=9999&amp;fos=6</LinkUrl>
        <CouponCode />
        <CouponRestrictions xsi:nil="true" />
        <StartDate xsi:nil="true" />
        <EndDate xsi:nil="true" />
        <ImageUrl xsi:nil="true" />
        <BannerWidth xsi:nil="true" />
        <BannerHeight xsi:nil="true" />
        <HtmlCode>&lt;a href="https://track.flexlinkspro.com/g.ashx?foid=2.4942550.14487458&amp;trid=177.168490&amp;foc=12&amp;fot=9999&amp;fos=6"&gt;Men's Shoe Nike Blazer Mid '77 Vintage, Shop Nike.com&lt;/a&gt;</HtmlCode>
        <AllowsDeeplinking>true</AllowsDeeplinking>
        <Categories>Footwear,Apparel,Sportswear</Categories>
        <Epc7D xsi:nil="true" />
        <Epc3M xsi:nil="true" />
        <PercentageOff>0</PercentageOff>
        <DollarOff>0</DollarOff>
        <LogoURL>https://content.flexlinks.com/sharedimages/programs/986021.png</LogoURL>
      </LinkDto>
      <LinkDto>
        <AdvertiserId>168490</AdvertiserId>
        <AdvertiserName>NIKE</AdvertiserName>
        <LinkId>2.4942550.14487499</LinkId>
        <LinkType>Text Link</LinkType>
        <LinkName>Men's Shoe Nike Blazer Low '77 Vintage, Shop Nike.com</LinkName>
        <LinkDescription>Men's Shoe Nike Blazer Low '77 Vintage, Shop Nike.com</LinkDescription>
        <PromotionalTypes>General Promotion</PromotionalTypes>
        <LinkUrl>https://track.flexlinkspro.com/g.ashx?foid=2.4942550.14487499&amp;trid=177.168490&amp;foc=12&amp;fot=9999&amp;fos=6</LinkUrl>
        <CouponCode />
        <CouponRestrictions xsi:nil="true" />
        <StartDate xsi:nil="true" />
        <EndDate xsi:nil="true" />
        <ImageUrl xsi:nil="true" />
        <BannerWidth xsi:nil="true" />
        <BannerHeight xsi:nil="true" />
        <HtmlCode>&lt;a href="https://track.flexlinkspro.com/g.ashx?foid=2.4942550.14487499&amp;trid=177.168490&amp;foc=12&amp;fot=9999&amp;fos=6"&gt;Men's Shoe Nike Blazer Low '77 Vintage, Shop Nike.com&lt;/a&gt;</HtmlCode>
        <AllowsDeeplinking>true</AllowsDeeplinking>
        <Categories>Footwear,Apparel,Sportswear</Categories>
        <Epc7D xsi:nil="true" />
        <Epc3M xsi:nil="true" />
        <PercentageOff>0</PercentageOff>
        <DollarOff>0</DollarOff>
        <LogoURL>https://content.flexlinks.com/sharedimages/programs/986021.png</LogoURL>
      </LinkDto>
    </Results>
    <PageNumber>1</PageNumber>
    <PageSize>10</PageSize>
    <TotalCount>2</TotalCount>
    <ResultType>Success</ResultType>
  </PaginatedResultSetOfLinkDto>"""
        
        mock_response = MagicMock()
        mock_response.text = mock_xml
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        result_json = server.get_flexoffers_promotions.fn(name="nike shoe")
        result = json.loads(result_json)
        
        # Verify result structure
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['total_count'], '2')
        self.assertEqual(len(result['data']), 2)
        
        # Verify first item fields
        item1 = result['data'][0]
        self.assertEqual(item1['AdvertiserId'], '168490')
        self.assertEqual(item1['AdvertiserName'], 'NIKE')
        self.assertEqual(item1['LinkName'], "Men's Shoe Nike Blazer Mid '77 Vintage, Shop Nike.com")
        self.assertEqual(item1['LinkDescription'], "Men's Shoe Nike Blazer Mid '77 Vintage, Shop Nike.com")
        self.assertEqual(item1['PromotionalTypes'], 'General Promotion')
        self.assertEqual(item1['LinkUrl'], "https://track.flexlinkspro.com/g.ashx?foid=2.4942550.14487458&trid=177.168490&foc=12&fot=9999&fos=6")

        # Verify second item fields
        item2 = result['data'][1]
        self.assertEqual(item2['LinkName'], "Men's Shoe Nike Blazer Low '77 Vintage, Shop Nike.com")

if __name__ == '__main__':
    unittest.main()
