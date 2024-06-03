package cmd

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/Sxl07/Client/functions"
	"github.com/spf13/cobra"
)

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
		fmt.Println("shutdown called")
		if password == "" {
			fmt.Println("a password is require use -p 'password'")
		}

		if password != "admin" {
			fmt.Println("Incorrect password")
		}

		request := Requests{
			Problem:  "",
			Cant:     0,
			Min:      0,
			Max:      0,
			Result:   "",
			Shutdown: 1,
			Password: password,
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

		var response Response
		err = json.NewDecoder(conn).Decode(&response)
		if err != nil {
			fmt.Println("Error al decodificar la respuesta JSON:", err)
		}
		fmt.Println("Respuesta del servidor:", response.Result)

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
	shutdownCmd.Flags().StringVarP(&password, "password", "p", "", "the password to authenticate shutdown")
}
