/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/Sxl07/Client/functions"
	"github.com/spf13/cobra"
)

type Response struct {
	Result []string `json:"result"`
}

type Requests struct {
	Problem  string
	Cant     int
	Min      int
	Max      int
	Result   string
	Shutdown int
	Password string
}

var problem string
var cant int
var min int
var max int
var result string

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "Client",
	Short: "A brief description of your application",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	Run: func(cmd *cobra.Command, args []string) {
		request := Requests{
			Problem:  problem,
			Cant:     cant,
			Min:      min,
			Max:      max,
			Result:   result,
			Shutdown: 0,
			Password: "",
		}

		port := "localhost:8080"
		conn, err := functions.OnServer(port)
		if err != nil {
			fmt.Println("Error:", err)
		}

		jsonData, err := json.Marshal(request)

		if err != nil {
			fmt.Println("error:", err)
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

		fmt.Println("Respuesta del servidor:", response)

		if result == "y" {
			fileName := "results.txt"

			content := strings.Join(response.Result, "\n")

			file, err := os.OpenFile(fileName, os.O_WRONLY|os.O_TRUNC, 0644)
			if err != nil {
				fmt.Println("Error al abrir el archivo:", err)
				return
			}
			defer file.Close()

			_, err = file.WriteString(content)
			if err != nil {
				fmt.Println("Error al escribir en el archivo:", err)
				return
			}

			fmt.Println("Archivo creado exitosamente.")
		}
		conn.Close()
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	// rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.Client.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	rootCmd.Flags().StringVarP(&problem, "problem", "p", "fizzbuzz", "Problem to be resolved")
	rootCmd.Flags().IntVarP(&cant, "quantity", "q", 25, "quantity of numbers")
	rootCmd.Flags().IntVarP(&min, "inflimit", "i", 0, "minimum number")
	rootCmd.Flags().IntVarP(&max, "suplimit", "s", 100, "maximum number")
	rootCmd.Flags().StringVarP(&result, "result", "r", "", "output file")
}
