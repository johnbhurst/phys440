#!/usr/bin/env -S dotnet fsi
// Copyright 2023 John Hurst
// John Hurst (john.b.hurst@gmail.com)
// 2023-12-16

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
    { State = rule.NewState;
      Tape = List.updateAt machine.Position rule.NewSymbol machine.Tape;
      Position = machine.Position + rule.Direction }

let program = System.IO.File.ReadLines(fsi.CommandLineArgs.[1])
            |> Seq.map parseRule

let tape = List.concat [("start" :: List.skip 2 (List.ofSeq fsi.CommandLineArgs)); ["blank"; "blank"; "blank"]]

let iterate (machine:Machine) =
    if machine.State = "qh" then None
    else
        Seq.filter (matchRule machine) program |> Seq.map (applyRule machine) |> Seq.map (fun machine -> (machine, machine)) |> Seq.tryHead

let machine = { State = "qs"; Tape = tape; Position = 0 }

let steps = List.unfold iterate machine

steps |> List.iter (fun machine -> printfn "%A" machine.Tape)