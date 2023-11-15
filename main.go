package main

import (
	"log"
	"net/http"
	"text/template"
)

// Templates
var templates = template.Must(template.ParseFiles("templates/index.html", "templates/idle.html"))

// Handler for the root path
func rootHandler(w http.ResponseWriter, r *http.Request) {
	err := templates.ExecuteTemplate(w, "index.html", nil)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func main() {
	// Serve static files
	fs := http.FileServer(http.Dir("./static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Route for the root path
	http.HandleFunc("/", rootHandler)

	// Start the server
	log.Println("Listening on :8080...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
