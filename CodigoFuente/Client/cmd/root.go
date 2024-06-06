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

		bad := false
		if problem == "" {
			fmt.Println("Problem cannot be empty")
			bad = true
		}
		if cant < 1 {
			fmt.Println("Quantity cannot be less than 1")
			bad = true
		}
		if min < 0 {
			fmt.Println("Low limit cannot be negative")
			bad = true
		}
		if max < min {
			fmt.Println("Superior limit cannot be less than low limit")
			bad = true
		}

		if !bad {
			err = functions.SendData(jsonData, conn)
			if err != nil {
				fmt.Println("Error:", err)
			}

			response, err := functions.DataResponse(conn)
			if err != nil {
				fmt.Println(err)
			}
			fmt.Println(response.Result)

			if result == "y" || result == "Y" {
				fileName := "results.txt"

				content := strings.Join(response.Result, "\n")

				file, err := os.OpenFile(fileName, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
				if err != nil {
					fmt.Println("Error opening the file:", err)
				}
				defer file.Close()

				_, err = file.WriteString(content)
				if err != nil {
					fmt.Println("Error writing in the file:", err)
				}
				fmt.Println("File results.txt Created.")
				fmt.Println("Your results are on the results.txt file.")
			}
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
	rootCmd.Flags().StringVarP(&problem, "problem", "p", "fizzbuzz", "Problem to be resolved fizzbuzz|fibonacci|prime")
	rootCmd.Flags().IntVarP(&cant, "quantity", "q", 25, "quantity of numbers")
	rootCmd.Flags().IntVarP(&min, "lowlimit", "l", 0, "minimum number of the range")
	rootCmd.Flags().IntVarP(&max, "suplimit", "s", 100, "maximum number of the range")
	rootCmd.Flags().StringVarP(&result, "result", "r", "", "save results in results.txt file, if you want to save results enter '-r (y/n)'. Results printed on console by default")
}
