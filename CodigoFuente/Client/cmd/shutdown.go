package cmd

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"

	"github.com/Sxl07/Client/functions"
	"github.com/spf13/cobra"
)

type Response struct {
	Result []string `json:"result"`
}

var password string

// shutdownCmd represents the shutdown command
var shutdownCmd = &cobra.Command{
	Use:   "shutdown",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		if password == "" {
			fmt.Println("a password is require use -p 'password'")
		}
		filename := "key.txt"

		secretKey, err := ioutil.ReadFile(filename)
		if err != nil {
			log.Fatalf("Error reading file: %v", err)
		}

		h := hmac.New(sha256.New, []byte(secretKey))
		h.Write([]byte(password))
		hash := h.Sum(nil)
		hashPassword := fmt.Sprintf("%x", hash)

		request := Requests{
			Problem:  "",
			Cant:     0,
			Min:      0,
			Max:      0,
			Result:   "",
			Shutdown: 1,
			Password: hashPassword,
		}

		port := "localhost:8080"
		conn, err := functions.OnServer(port)
		if err != nil {
			fmt.Println("Error:", err)
		}

		jsonData, err := json.Marshal(request)
		if err != nil {
			log.Fatalf("error: %v", err)
		}

		err = functions.SendData(jsonData, conn)
		if err != nil {
			fmt.Println("Error:", err)
		}

		response, err := functions.DataResponse(conn)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println(response.Result)
	},
}

func init() {
	rootCmd.AddCommand(shutdownCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// shutdownCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// shutdownCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	shutdownCmd.Flags().StringVarP(&password, "password", "p", "", "the password to authenticate shutdown,use -p 'password'")
}