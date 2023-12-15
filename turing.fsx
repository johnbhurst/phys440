#!/usr/bin/env -S dotnet fsi
// Copyright 2023 John Hurst
// John Hurst (john.b.hurst@gmail.com)
// 2023-12-16

// Simple Turing Machine simulator.
// Usage: turing.fsx <program> <tape>
// <program> is a file containing the rules for the machine. Each rule is a line containing 5 space-separated fields:
//   <state> <symbol> <new-state> <new-symbol> <direction>
// <tape> is a list of symbols separated by spaces.
// An example program is:
// qs start q1 start +1
// q1 0 q1 blank +1
// q1 1 q1 blank +1
// q1 blank q2 blank -1
// q2 blank q2 blank -1
// q2 start q3 start +1
// q3 blank qh 1 0
//
// 'qs' is the initial state.
// 'qh' is the halt state.
// 'start' is the initial symbol on the tape.
// Following the 'start' symbol on the tape is the input, as an arbitrary number of 0s and 1s.
// This program erases the input and prints a single "1" on the tape as the output.

type Rule = { State: string; Symbol: string; NewState: string; NewSymbol: string; Direction: int }

type Machine = { State: string; Tape: string list; Position: int }

// Parse a rule from an input line of text.
let parseRule (line:string) =
  let parts = line.Split(' ')
  { State = parts.[0];
    Symbol = parts.[1];
    NewState = parts.[2];
    NewSymbol = parts.[3];
    Direction = int parts.[4] }

// Predicate to determine if a rule matches the current machine state.
let matchRule (machine:Machine) (rule:Rule) =
    machine.State = rule.State && machine.Tape.[machine.Position] = rule.Symbol

// Update the machine according to the rule.
let applyRule (machine:Machine) (rule:Rule) =
    let newTape = List.updateAt machine.Position rule.NewSymbol machine.Tape
    let newPosition = machine.Position + rule.Direction
    { State = rule.NewState;
      Tape = if newPosition >= newTape.Length then newTape @ ["blank"] else newTape;
      Position = newPosition }

// Read the first command line arg as a file containing the list of rules making up the program.
let program = System.IO.File.ReadLines(fsi.CommandLineArgs.[1])
            |> Seq.map parseRule

// Read the remaining command line args as the tape input.
let tape = "start" :: List.skip 2 (List.ofSeq fsi.CommandLineArgs)

// Iterate the machine until it halts.
let iterate (machine:Machine) =
    if machine.State = "qh" then None
    else
        program |> Seq.filter (matchRule machine)
                |> Seq.map (applyRule machine)
                |> Seq.map (fun machine -> (machine, machine))
                |> Seq.tryHead

// Run the machine and print the tape at each step.
List.unfold iterate { State = "qs"; Tape = tape; Position = 0 }
            |> List.map (fun machine -> machine.Tape)
            |> List.iter (printfn "%A")
