RequirePackage <- function (function_name){
  function_name <- as.character(function_name)
  
  if (!require(function_name,character.only = TRUE))
  {
    print("Installing package")
    install.packages(function_name)
    print("Loading package...")
    require(function_name,character.only = TRUE)
  } else {
    require(function_name,character.only = TRUE)
  }
}
RequirePackage("shiny") #Loading Shiny package

# User Interface: The user interface contains all input- and output controls which are rendered by the server function.
ui <- fluidPage(
  navbarPage(title ="HIVE", theme = "honeycomb.css",
             tabPanel("Home",
                      column(4, align="center", style='margin-top: 80px;', offset = 4,
                            imageOutput("application_image", width = "180px", height = "70px"),
                            h3("Welcome at HIVE"),
                            p("Please use the navigation-bar to navigate to the right module and start using HIVE. Please contact us if you needs assistance"),
                            tags$style(type="text/css", "#string { height: 50px; width: 100%; text-align:center; font-size: 30px; display: block;}")
                      )
                      ),
             tabPanel("Panel"
             ),
             navbarMenu("Settings",
                        tabPanel("Status"
                        ),
                        tabPanel("Keywords",
                                 tableOutput("keywordtable")
                        ),
                        tabPanel("Help"
                        )
             )
             )
  )

# Server: The server function contains functions to render the in- and output elements. 
server <- function(input, output, session){

  
  
  # Home TAB
  output$application_image <- renderImage({
      return(list(
        src = "assets/application_logo.png",
        contentType = "application_logo.png",
        width = "100%",
        alt = "Application Logo"
      ))
  }, deleteFile = FALSE)
}
  
shinyApp(server = server, ui = ui, options = list(port = 8080))
