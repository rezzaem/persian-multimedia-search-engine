from openai import OpenAI

YOUR_API_KEY = "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"

system_prompt = """You are an AI assistant that uses the Perplexity API to analyze video metadata and generate a summary and important information about the video. You will receive three inputs: a user query, a video title, and a video description. You should use this information to generate a concise and informative description of the video.
The output should be a list with two indices: [0/1, "ok"/"filtered", "video summary and information"].
The first index indicates whether the video content is against Iran's internet rules (1 = filtered, 0 = ok).
The second index provides a brief summary and important information about the video, written in Persian language.
Please respond with your analysis of the video metadata, using the format [0/1, "ok"/"filtered", "video summary and information"].
For example, if the inputs are:
User query: "mental health"
Video title: "5 Ways to Improve Your Mental Health"
Video description: "In this video, we'll explore five simple yet effective ways to improve your mental health and wellbeing."
The output could be:
[0, "ok", "این ویدئو پنج روش ساده اما موثر برای بهبود سلامت روان و بهزیستی را معرفی می کند. از تکنیک های مدیریت استرس تا روش های ارتباط با دیگران، این ویدئو اطلاعات مفید و عملی را برای بهبود سلامت روان ارائه می دهد."]"""

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

while True:
    query="User query:"+input("query : ")
    title="Video title:"+input("title : ")
    desc_yout="""با مجید حسامی، مدیرعامل و بنیانگذار اسنپ‌پی، در مورد پیدایش اسنپ‌پی و طرح 'الان خرید کن، بعدا پرداخت کن' به گفتگو نشستیم. درباره صنعت فین‌تک و استفاده از داده‌های اسنپ برای راه‌اندازی یک سیستم اعتبارسنجی مالی در ایران، جایی که سیستم کارت‌های اعتباری وجود نداره، بحث کردیم و اینکه چگونه مردم میتونند از این سیستم برای خرید استفاده و در پایان ماه پرداخت کنن. همچنین در مورد اینکه چگونه این مسیر به تبدیل شدن به یک پلتفرم ای‌کامرس منجر شد، صحبت شد.

We sat down with Majid Hesami, founder and CEO of SnappPay, to discuss the creation of SnappPay and the 'buy now, pay later' plan. We talked about the fintech industry and using Snapp's data to launch a financial credit scoring system in Iran, where credit card systems do not exist, and how people can use this system to make purchases and pay at the end of the month. We also discussed how this pathway has evolved into an e-commerce platform.

مهمان: مجید حسامی (مدیرعامل و بنیانگذار اسنپ‌پی)
برنامه: پادکست طبقه ۱۶
اسپانسر: خدمات رایانش ابری لیارا (https://liara.ir)
شبکه‌های پخش: Castbox، Spotify، و سایر پلتفرم‌ها
هشتگ‌ها: #پادکست #طبقه۱۶"""
    desc="Video description:"+desc_yout
    lst=list()
    lst.append(query)
    lst.append(title)
    lst.append(desc)
    user_input = f"{query}\n{title}\n{desc}"
    # if user_input.lower() == 'q':
    #     break

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="llama-3-sonar-small-32k-online",
        messages=messages,
    )
    system_response = response.choices[0].message.content
    print(system_response)