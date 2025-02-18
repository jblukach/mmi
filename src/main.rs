use colored::Colorize;
use poppy_filters::v2::BloomFilter;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 {
        if args[1] == "download" {
            mmi::download();
        } else if args[1] == "status" {
            mmi::status();
        } else if args[1] == "verify" {
            mmi::verify();
        } else {
            println!("Commands: download, status, verify");
        }
    } else {
        let lolpath = std::env::current_exe().unwrap().parent().unwrap().join("lol.poppy");
        let mmipath = std::env::current_exe().unwrap().parent().unwrap().join("mmi.poppy");
        if std::path::Path::new(&lolpath).exists() && std::path::Path::new(&mmipath).exists() {
            let lolfile = std::fs::File::open(&lolpath).unwrap();
            let lolpoppy = BloomFilter::from_reader(lolfile).unwrap();
            let mmifile = std::fs::File::open(&mmipath).unwrap();
            let mmipoppy = BloomFilter::from_reader(mmifile).unwrap();
            if let Ok(entries) = std::fs::read_dir(".") {
                for entry in entries {
                    if let Ok(entry) = entry {
                        let directory = std::env::current_dir().unwrap();
                        let filename = entry.file_name();
                        let fullpath = directory.join(&filename);
                        let b3dir;
                        let b3path;
                        let mut separator: String;
                        if cfg!(target_os = "windows") {
                            b3path = mmi::b3windows(fullpath.display().to_string());
                            b3dir = mmi::b3windows(directory.display().to_string());
                            separator = "\\".to_string();
                        } else {
                            b3path = mmi::b3unix(fullpath.display().to_string());    
                            b3dir = mmi::b3unix(directory.display().to_string());
                            separator = "/".to_string();
                        }
                        let b3name = mmi::b3text(filename.to_string_lossy().to_string());
                        let mut b3hash;
                        if fullpath.is_dir() {
                            b3hash = "  -- DIRECTORY --                                               ".to_string();
                        } else {
                            let test = std::fs::File::open(entry.path());
                            if test.is_err() {
                                b3hash = "  -- DENIED --                                                  ".red().to_string();                                
                            } else {
                                let metadata = std::fs::metadata(fullpath.clone()).unwrap();
                                let fsize = metadata.len().to_string();
                                if fsize == "0" {
                                    b3hash = "  -- ZERO --                                                    ".to_string();
                                } else if fsize.parse::<u64>().unwrap() > 10*104857599 { // 1GB
                                    b3hash = "  -- LARGE --                                                   ".red().to_string();
                                } else {
                                    b3hash = mmi::b3content(&fullpath);
                                    if b3hash == "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262" {
                                        b3hash = "  -- EMPTY --                                                   ".to_string();
                                    } else if b3hash == "ERROR" {
                                        b3hash = "  -- ERROR --                                                   ".red().to_string();
                                    } else {
                                        b3hash = b3hash;
                                    }
                                }
                            }
                        }
                        if lolpoppy.contains(&b3hash) == true {
                            b3hash = b3hash.red().to_string();
                        } else if mmipoppy.contains(&b3hash) == true {
                            b3hash = b3hash.green().to_string();
                        } else {
                            b3hash = b3hash;
                        }
                        let mut directory = directory.display().to_string();
                        let mut filename = filename.to_string_lossy().to_string();
                        if lolpoppy.contains(&b3path) == true {
                            directory = directory.red().to_string();
                            separator = separator.red().to_string();
                            filename = filename.red().to_string();
                        } else if mmipoppy.contains(&b3path) == true {
                            directory = directory.cyan().to_string();
                            separator = separator.cyan().to_string();
                            filename = filename.cyan().to_string();
                        } else {
                            separator = separator;
                            if mmipoppy.contains(&b3dir) == true {
                                directory = directory.cyan().to_string();
                                separator = separator.magenta().to_string();
                            } else {
                                directory = directory;
                            }
                            if lolpoppy.contains(&b3name) == true {
                                separator = separator.magenta().to_string();
                                filename = filename.red().to_string();
                            } else if mmipoppy.contains(&b3name) == true {
                                separator = separator.magenta().to_string();
                                filename = filename.cyan().to_string();
                            } else {
                                filename = filename;
                            }
                        }
                        println!("{} {}{}{}", b3hash, directory, separator, filename);
                    }
                }
            }
        } else {
            println!("Required File: {}", lolpath.display());
            println!("Required File: {}", mmipath.display());
            println!("Download Link: https://github.com/jblukach/artifacts/releases");
        }
    }
}