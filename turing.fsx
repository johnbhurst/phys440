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

let parseRule (line:string) =
  let parts = line.Split(' ')
  { State = parts.[0];
    Symbol = parts.[1];
    NewState = parts.[2];
    NewSymbol = parts.[3];
    Direction = int parts.[4] }

let matchRule (machine:Machine) (rule:Rule) =
    machine.State = rule.State && machine.Tape.[machine.Position] = rule.Symbol

let applyRule (machine:Machine) (rule:Rule) =
    let newTape = List.updateAt machine.Position rule.NewSymbol machine.Tape
    let newPosition = machine.Position + rule.Direction
    { State = rule.NewState;
      Tape = if newPosition >= newTape.Length then newTape @ ["blank"] else newTape;
      Position = newPosition }

let program = System.IO.File.ReadLines(fsi.CommandLineArgs.[1])
            |> Seq.map parseRule

let tape = "start" :: List.skip 2 (List.ofSeq fsi.CommandLineArgs)

let iterate (machine:Machine) =
    if machine.State = "qh" then None
    else
        program |> Seq.filter (matchRule machine)
                |> Seq.map (applyRule machine)
                |> Seq.map (fun machine -> (machine, machine))
                |> Seq.tryHead

List.unfold iterate { State = "qs"; Tape = tape; Position = 0 }
            |> List.map (fun machine -> machine.Tape)
            |> List.iter (printfn "%A")
