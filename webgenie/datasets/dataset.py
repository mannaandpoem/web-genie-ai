from pydantic import Field, BaseModel

class DatasetEntry(BaseModel):
    src: str = Field(default="", description="The source of the dataset entry")
    topic: str = Field(default="", description="The topic of the dataset entry")
    ground_truth_html: str = Field(default="", description="The ground truth html")
    prompt: str = Field(default="", description="The prompt for the text task")
    base64_image: str = Field(default="", description="The base64 encoded image")

class Dataset:
    async def generate_context(self)->DatasetEntry:
        pass

class MockUpDataset(Dataset):
    async def generate_context(self)->DatasetEntry:
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Tech Company</title>
<style>
    body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #fff;
    background-color: #1a2632;
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: #1a2632;
}

.header-container .logo {
    font-size: 24px;
}

nav ul {
    list-style: none;
    display: flex;
    gap: 20px;
}

nav ul li a {
    color: #fff;
    text-decoration: none;
}

.hero {
    width: 100%;
    height: auto;
}

.hero img {
    width: 100%;
    height: auto;
}

.welcome {
    text-align: center;
    padding: 40px;
    background-color: #1a2632;
}

.welcome h1 {
    font-size: 36px;
    margin-bottom: 20px;
}

.welcome p {
    font-size: 16px;
    line-height: 1.5;
    max-width: 600px;
    margin: 0 auto;
}

footer {
    padding: 20px;
    background-color: #28323c;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

footer p {
    margin: 0;
}

.footer-container .socials a {
    color: #fff;
    text-decoration: none;
    margin-left: 20px;
}
</style>
<link href="styles.css" rel="stylesheet"/>
</head>
<body>
<header>
<div class="header-container">
<div class="logo">Tech Company</div>
<nav>
<ul>
<li><a href="#">Home</a></li>
<li><a href="#">About</a></li>
<li><a href="#">Products</a></li>
<li><a href="#">Contact</a></li>
</ul>
</nav>
</div>
</header>
<section class="hero">
<img alt="Hero Image" src="https://picsum.photos/seed/picsum/800/600"/>
</section>
<section class="welcome">
<h1>Welcome to Tech Company</h1>
<p>At Tech Company, we are dedicated to providing the best technology solutions for your needs. Our team of experts is always ready to help you with any questions or problems you may have.</p>
</section>
<footer>
<div class="footer-container">
<p>© 2022 Tech Company. All rights reserved.</p>
<div class="socials">
<a href="#">Facebook</a>
<a href="#">Twitter</a>
<a href="#">Instagram</a>
</div>
</div>
</footer>
</body>
</html>
        """
        return DatasetEntry(
            src="mockup",
            topic="tech company",
            ground_truth_html=html,
            prompt="",
            base64_image=""
        )

class MockUpPromptDataset(Dataset):
    async def generate_context(self)->DatasetEntry:
        return DatasetEntry(
            src="mockup",
            topic="tech company",
            ground_truth_html="",
            prompt="CommingSoon Page with goback button, navHeader, and footer",
            base64_image=""
        )