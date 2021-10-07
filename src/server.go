package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type Password struct {
	Password string
}

var ADMIN_PASSWORD string = "ababacaabbcbcababacaabbcbc"

func adminLogin(w http.ResponseWriter, req *http.Request) {
	var pass Password

	err := json.NewDecoder(req.Body).Decode(&pass)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if pass.Password == ADMIN_PASSWORD {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Ok"))
	} else {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("Wrong Password"))
	}
}

func main() {
	http.HandleFunc("/admin/login", adminLogin)
	fmt.Println("server listening on port 5000")
	http.ListenAndServe(":5000", nil)
}
