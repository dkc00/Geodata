# Build a Shiny app to display spectrometer data

# At the beginning, the necessary libraries are invited.
library(shiny)
# Shinythemes is used to visually enhance the Shiny app. 
library(shinythemes)

# The folder "Installation_Mosel_24", where the spectrometer data from the FTP server is stored locally, is accessed here.
# Recursively search for the files in all subfolders from there. 
# datenordner <- "..."

# Sets the working directory to the data folder
setwd(datenordner)

# For the above reason, we set recursive to TRUE. full.names for the file path could also be set to FALSE, 
# depending on which display you want. Since the name of the subfolder will also be displayed later for file_names and the file 
# should be better assigned, I have left it like this.

file_paths_all <- list.files(pattern = "\\.csv$", recursive = TRUE, full.names = TRUE)

file_paths <- list.files(pattern = "Reflectance.*\\.csv$", recursive = TRUE, full.names = TRUE)
file_names <- sub(paste0(datenordner, "/"), "", file_paths)

# This is where the UI is defined. fluidPage is used to scale the components of the homepage in real time. 
# suitable Shinytheme for the appearance of the app. This can be changed as desired.

ui <- fluidPage(
  theme = shinytheme("united"),
  
  # The title, a sidebar for selecting the file, the main panel with the spectrum as a plot and the rest of the structure follow 
  # consisting of headings with simple HTML code, buttons for loading the other spectra and for plotting NDCI vs. NDVI. 
  # Potentially you could insert any plot here, depending on the purpose of the display for the evaluation.
  
  titlePanel("RoX spectrometer data"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("file", "Select file:", file_names)
    ),
    
    mainPanel(
      h3("Spectra: "),
      plotOutput("spectrumPlot"),
    
      h4(HTML("<u> 2. Reflectance values: Descriptive statistics (Spectral bands from 400nm until 900nm) </u>")),
      
      # The following uiOutput elements are further described and defined in the server logic.
      uiOutput("statistik"),
      
      h4(HTML("<u> 3. Environmental indices: </u>")),
      
      h5(HTML("<b>NDCI (Normalized Difference Chlorophyll Index):</b> ")),
      uiOutput("formula_ndci"),
      uiOutput("result_ndci"),
      NULL,
      
      h5(HTML("<b>NDVI (Normalized Difference Vegetation Index):</b> ")),
      uiOutput("formula_ndvi"),
      uiOutput("result_ndvi"),
      NULL,
      h5(HTML("<b>SABI (Surface Algae Blooms Index):</b> ")),
      uiOutput("formula_sabi"),
      uiOutput("result_sabi"),
      NULL,
      h5(HTML("<b>BNDVI (Blue Normalized Difference Vegetation Index):</b> ")),
      uiOutput("formula_bndvi"),
      uiOutput("result_bndvi"),
      NULL,
      HTML("<br><br>"),
      
      actionButton("ndci_vs_ndvi", "Plot NDCI vs. NDVI", type = "primary", class = "btn-xs"),
      plotOutput("ndci_vs_ndvi_plot"),
      
      NULL,
    )
  )
)

# In the second step, the server logic is defined. This is where the code required for the UI is written.

server <- function(input, output) {
  
  
  observe({
    selected_file <- input$file
    
    # The selected file is displayed. Can help with debugging.
    print(paste0("Ausgewählte Datei: ", selected_file))
    
    # Asks whether a file has been selected
    if (!is.null(selected_file)) {
      
      # Which file was selected
      selected_file_path <- file_paths[which(file_names == selected_file)]
      
      # Only work with .csv (lower case). .CSV includes the raw data and .xlsx also crashes the program.
      # But this does not need to be changed at the moment as all final spectrometer data are .csv files.
      
      if (grepl("\\.csv$", selected_file_path, ignore.case = FALSE)) {
        # Attempts to read the csv file
        tryCatch({
          # Reads the file, header needs to be TRUE and the seperator is ; 
          daten <- read.csv(selected_file_path, header = TRUE, sep = ";", stringsAsFactors = FALSE)
          
          # Some numeric values were stored as "chr" data type. Hence this conversion to numeric values.
          daten <- data.frame(lapply(daten, function(x) {
            if (is.character(x)) {
              as.numeric(x)
            } else {
              x
            }
          }))
          
          
          # x is the wavelength and y the spectra
          x_values <- daten[, 1]
          y_values <- daten[, -1]
          
          # Code for the action button and the display of all spectra. 
          
          observeEvent(input$allespektren, {

            selected_file_paths <- file_paths_all[grepl("Reflectance|Incoming|Reflected", file_paths_all)]
            

            selected_data <- lapply(selected_file_paths, function(file) {
              tryCatch({
                read.csv(file, header = TRUE, sep = ";", stringsAsFactors = FALSE)
              }, error = function(e) {
                message(paste("Error loading the file:", file))
                NULL
              })
            })
            
            file_names_all <- sub(paste0(datenordner, "/"), "", file_paths_all)
            updateSelectInput(session, "file", choices = file_names_all)
            
          })
          
          # Statistical evaluation, preparation of a list and subsequent code  
          # for the various parameters.
          
          daten_means <- list()
          
          for (i in 1:ncol(y_values)) {
            actual_mean <- as.numeric(mean(y_values[x_values >= 400 & x_values <= 900, i], na.rm = TRUE))
            daten_means[[i]] <- actual_mean
            actual_min <- as.numeric(min(y_values[x_values >= 400 & x_values <= 900, i], na.rm = TRUE))
            daten_means[[i]] <- actual_min
            actual_max <- as.numeric(max(y_values[x_values >= 400 & x_values <= 900, i], na.rm = TRUE))
            daten_means[[i]] <- actual_max
            actual_median <- as.numeric(median(y_values[x_values >= 400 & x_values <= 900, i], na.rm = TRUE))
            daten_means[[i]] <- actual_median
            actual_firstq <- as.numeric(quantile(y_values[x_values >= 400 & x_values <= 900, i], 0.25,  na.rm = TRUE))
            daten_means[[i]] <- actual_firstq
            actual_thirdq <- as.numeric(quantile(y_values[x_values >= 400 & x_values <= 900, i], 0.75, na.rm = TRUE))
            daten_means[[i]] <- actual_thirdq
            actual_std <- as.numeric(sd(y_values[x_values >= 400 & x_values <= 900, i], na.rm = TRUE))
            daten_means[[i]] <- actual_std
            actual_var <- as.numeric(var(y_values[x_values >= 400 & x_values <= 900, i], na.rm = TRUE))
            daten_means[[i]] <- actual_var
            
          }
          
          output$statistik <- renderText({
            
            paste("Mean:", actual_mean, "<br>",
                  "Min value:", actual_min, "<br>",
                  "Max value: ", actual_max, "<br>",
                  "Median: ", actual_median, "<br>",
                  "1st quartile: ", actual_firstq, "<br>",
                  "3rd quartile:", actual_thirdq, "<br>",
                  "Standard deviation: ", actual_std, "<br>",
                  "Variance: ", actual_var, "<br><br>")
            
            
          })
          
          output$formula_ndci <- renderText({
            "NDCI = (R(708nm) - R(665nm)) / (R(708nm) + R(665nm)) "
          })
          
          ndci_list <- list()
          
          for (i in 1:ncol(y_values)) {
            
            # Convert the y values to numerical values 
            y_col <- as.numeric(y_values[, i])
            
            x_708 <- y_col[floor(x_values) == 708]
            x_665 <- y_col[floor(x_values) == 665]
            
            # Average reflectances
            #na.rm = TRUE, because there may be NA values in the code and it should still work. 
            ref_708 <- mean(x_708, na.rm = TRUE)
            ref_665 <- mean(x_665, na.rm = TRUE)
            
            ndci <- (ref_708 - ref_665) / (ref_708 + ref_665)
            ndci_list[[i]] <- ndci
          }
          
          output$result_ndci <- renderPrint({
            ndci
          })
          
          
          output$formula_ndvi <- renderText({
            "NDVI = (R(800nm) - R(670nm)) / (R(800nm) + R(670nm)) "
          })
          
          ndvi_list <- list()
          
          for (i in 1:ncol(y_values)) {
            
            # Convert the y values to numerical values  
            y_col <- as.numeric(y_values[, i])
            
            x_800 <- y_col[floor(x_values) == 800]
            x_670 <- y_col[floor(x_values) == 670]
            
            # Average reflectances
            #na.rm = TRUE, because there may be NA values in the code and it should still work. 
            ref_800 <- mean(x_800, na.rm = TRUE)
            ref_670 <- mean(x_670, na.rm = TRUE)
            
            ndvi <- (ref_800 - ref_670) / (ref_800 + ref_670)
            ndvi_list[[i]] <- ndvi
          }
          
          output$result_ndvi <- renderPrint({
            ndvi
            
          })
          
          
          output$formula_sabi <- renderText({
            "SABI = (R(800nm) - R(670nm))/ (R(450nm) + R(550nm)) "
            # (NIR-R)/(B+G)
          })
          
          sabi_list <- list()
          
          for (i in 1:ncol(y_values)) {
            
            #
            y_col <- as.numeric(y_values[, i])
            
            x_800 <- y_col[floor(x_values) == 800]
            x_670 <- y_col[floor(x_values) == 670]
            x_450 <- y_col[floor(x_values) == 450]
            x_550 <- y_col[floor(x_values) == 550]
            
            
            ref_800 <- mean(x_800, na.rm = TRUE)
            ref_670 <- mean(x_670, na.rm = TRUE)
            ref_450 <- mean(x_450, na.rm = TRUE)
            ref_550 <- mean(x_550, na.rm = TRUE)
            
            sabi <- (ref_800 - ref_670) / (ref_450 + ref_550)
            sabi_list[[i]] <- sabi
          }
          
          output$result_sabi <- renderPrint({
            sabi
            
          })
          
          output$formula_bndvi <- renderText({
            "BNDVI = (R(800nm) - R(450nm)) / (R(800nm) + R(450nm)) "
            # (NIR-B)/(NIR+B)
          })
          
          bndvi_list <- list()
          
          for (i in 1:ncol(y_values)) {
            
            y_col <- as.numeric(y_values[, i])
            
            x_800 <- y_col[floor(x_values) == 800]
            x_450 <- y_col[floor(x_values) == 450]
            
            ref_800 <- mean(x_800, na.rm = TRUE)
            ref_450 <- mean(x_450, na.rm = TRUE)
            
            bndvi <- (ref_800 - ref_450) / (ref_800 + ref_450)
            bndvi_list[[i]] <- bndvi
          }
          
          output$result_bndvi <- renderPrint({
            bndvi
            
          })
          
          observeEvent(input$ndci_vs_ndvi, {
            # Lists for all NDCI and NDVI values
            ndci_values <- list()
            ndvi_values <- list()
            
            for (i in 1:ncol(y_values)) {
              y_col <- as.numeric(y_values[, i])
              
              x_708 <- y_col[floor(x_values) == 708]
              x_665 <- y_col[floor(x_values) == 665]
              ref_708 <- mean(x_708, na.rm = TRUE)
              ref_665 <- mean(x_665, na.rm = TRUE)
              ndci <- (ref_708 - ref_665) / (ref_708 + ref_665)
              
              x_800 <- y_col[floor(x_values) == 800]
              x_670 <- y_col[floor(x_values) == 670]
              ref_800 <- mean(x_800, na.rm = TRUE)
              ref_670 <- mean(x_670, na.rm = TRUE)
              ndvi <- (ref_800 - ref_670) / (ref_800 + ref_670)
              
              
              ndci_values[[i]] <- ndci
              ndvi_values[[i]] <- ndvi
            }
            
            # An example NDCI vs. NDVI plot is generated. Can be changed
            # with the desired index. 
            output$ndci_vs_ndvi_plot <- renderPlot({
              plot(unlist(ndci_values), unlist(ndvi_values),
                   xlab = "NDCI", ylab = "NDVI",
                   main = "NDCI vs. NDVI",
                   xlim = c(-0.1, 0), ylim = c(-0.3, 0))
            })
          })
          
          
          # Finally, the plot for the respective spectrum is created with Matplot.
          
          output$spectrumPlot <- renderPlot({
            matplot(x_values, y_values, type = "l", lty = 1, col = 1:ncol(y_values),
                    xlab = "Wavelength [nm]", ylab = "Reflectance", main = paste0(basename(selected_file)),
                    xlim = c(400,900), ylim = c(0, 0.1))
          })
          
        } 
        )
      }
    }
  })
}
# Load the app 
shinyApp(ui = ui, server = server)
