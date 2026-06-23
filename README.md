<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RichardGabelman/ca-tenant-law-rag">
    <img src="frontend/public/calitenantrights_logo_tight.svg" alt="Logo" width="100" height="100">
  </a>

<h3 align="center">California Tenant Rights RAG</h3>

  <p align="center">
    A RAG-powered web app that helps California tenants understand their legal rights. Describe your situation in plain English and get a cited, AI-generated answer drawn from the most relevant sections of California law, with source cards linking directly to the official legislative code.
    <br />
    <br />
    <a href="https://calitenantrights.richardgabelman.com">View Live</a>
    &middot;
    <a href="https://github.com/RichardGabelman/ca-tenant-law-rag/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

<div align="center">
  <a href="https://calitenantrights.richardgabelman.com">
    <img src="images/page_screenshot.png" alt="California Tenant Rights RAG UI">
  </a>
</div>

<br />
<br />

<p>
California tenant law is dense, scattered across different code sections, and difficult to navigate without a legal background. Renters facing issues with deposits, habitability, evictions, or lease disputes often don't know where to start or even what questions to ask.
</p>

<p>
<b>California Tenant Rights RAG</b> makes that body of law searchable in plain English. Describe your situation and the app returns a plain-language answer citing the specific sections of the California Civil and Health & Safety Code it drew from, alongside source cards with direct links to the official legislative text.
</p>

<p>
Under the hood, the relevant code sections are parsed, chunked, and embedded into a ChromaDB vector store using Sentence Transformers. At query time, the user's question is encoded into the same vector space and compared against stored embeddings using cosine similarity. The top matching sections are retrieved, deduplicated by section number, and passed as context to a Groq-hosted LLM, which synthesizes a grounded answer and returns the specific sections it cited. The FastAPI backend returns the answer, cited section numbers, and full source metadata to the React frontend.
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![React][React.js]][React-url]
- ![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
- ChromaDB
- Sentence Transformers
- Groq
- Frontend hosted on ![Vercel Badge](https://img.shields.io/badge/Vercel-000?logo=vercel&logoColor=fff&style=for-the-badge)
- Backend hosted on a <span>  </span> ![Hetzner Badge](https://img.shields.io/badge/Hetzner-D50C2D?logo=hetzner&logoColor=fff&style=for-the-badge) vps

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Groq API key.

### Installation

1. Clone the repo

```sh
   git clone https://github.com/RichardGabelman/ca-tenant-law-rag.git
```

2. Download the [pre-built ChromaDB here](https://github.com/RichardGabelman/ca-tenant-law-rag/releases/download/v1.0.0/chroma_db.zip) and extract it to `/backend/chroma_db`. This saves you from needing to run the ingestion pipeline and download the full California legislative dataset.

3. Set up the backend

```sh
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-prod.txt
```

4. Create a `.env` file in `/backend`

```
   CHROMA_DIR=./chroma_db
   ALLOWED_ORIGINS=http://localhost:5173
```

5. Start the backend

```sh
   uvicorn api.main:app --reload
```

6. Set up the frontend

```sh
   cd ../frontend
   npm install
```

7. Create a `.env` file in `/frontend`

```
   VITE_API_URL=http://localhost:8000
```

8. Start the frontend

```sh
   npm run dev
```

The app will be running at `http://localhost:5173`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Enter a plain-English description of your situation and submit. The app returns:

- A plain-language answer synthesized from the most relevant sections of California tenant law
- The specific code sections cited in the answer, highlighted among the source cards
- Direct citation links to each section on the official California legislative site

**Example queries:**
- *"My landlord hasn't returned my security deposit after 45 days"*
- *"My heater has been broken for weeks and my landlord won't fix it"*
- *"My landlord wants to enter my apartment tomorrow with no notice"*

<br />

[![California Tenant Rights RAG Usage Screen Shot][usage-screenshot]](images/usage_screenshot.png)

Try the live app at [calitenantrights.richardgabelman.com](https://calitenantrights.richardgabelman.com).


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->

## License

Distributed under the MIT. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Richard Gabelman - [@RichardGabelman](https://twitter.com/RichardGabelman) - hello@richardgabelman.com

Project Link: [https://github.com/RichardGabelman/ca-tenant-law-rag](https://github.com/RichardGabelman/ca-tenant-law-rag)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Groq](https://groq.com) - for the LLM API used to generate the section summaries and example questions during ingestion
- [ChromaDB](https://www.trychroma.com) - for the vector store
- [Sentence Transformers](https://www.sbert.net) - for the embedding model
- [California Legislative Information](https://leginfo.legislature.ca.gov) - the source of the legal dataset
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) - for the README template

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/RichardGabelman/ca-tenant-law-rag.svg?style=for-the-badge
[contributors-url]: https://github.com/RichardGabelman/ca-tenant-law-rag/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/RichardGabelman/ca-tenant-law-rag.svg?style=for-the-badge
[forks-url]: https://github.com/RichardGabelman/ca-tenant-law-rag/network/members
[stars-shield]: https://img.shields.io/github/stars/RichardGabelman/ca-tenant-law-rag.svg?style=for-the-badge
[stars-url]: https://github.com/RichardGabelman/ca-tenant-law-rag/stargazers
[issues-shield]: https://img.shields.io/github/issues/RichardGabelman/ca-tenant-law-rag.svg?style=for-the-badge
[issues-url]: https://github.com/RichardGabelman/ca-tenant-law-rag/issues
[license-shield]: https://img.shields.io/github/license/RichardGabelman/ca-tenant-law-rag.svg?style=for-the-badge
[license-url]: https://github.com/RichardGabelman/ca-tenant-law-rag/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/richard-gabelman
[product-screenshot]: images/page_screenshot.png
[usage-screenshot]: images/usage_screenshot.png

<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->

[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
