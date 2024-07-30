import streamlit as st

def main():
    st.title("Deva's Portfolio")
    st.write("Hey Devlopers.....!")

    # About Section
    st.header("About Me")
    st.write(
        """
        Hi, I'm Dev Anand, a passionate developer with expertise in various technologies. 
        I specialize in AI/ML, Python Full Stack, MERN Stack Development, FastAPI, and NGINX deployment.
        """
    )

    # Skills Section
    st.header("Technical Skills")
    skills = [
        "AI/ML",
        "Python Full Stack",
        "MERN Stack Development",
        "FastAPI",
        "NGINX Deployment"
    ]
    st.write(", ".join(skills))

    # Projects Section
    st.header("Projects")
    st.subheader("1. Smart Irrigation System")
    st.write(
        """
        A smart irrigation system using IoT and integrated with Blynk. 
        It includes water level sensor, NodeMCU ESP8266, flow sensor, and temperature sensor.
        """
    )
    
    st.subheader("2. Web Scraping and Data Collection")
    st.write(
        """
        A project for scraping content from a website and saving it in JSON format. 
        Utilizes Python and BeautifulSoup for data extraction.
        """
    )

    # Contact Section
    st.header("Contact")
    st.write(
        """
        You can reach me at:
        - Email: deva@example.com
        - LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/deva)
        """
    )

if __name__ == "__main__":
    main()
