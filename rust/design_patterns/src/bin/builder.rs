// use constraction_patterns::run;
use simple_pattern::run;

mod constraction_patterns {
    #[derive(Debug)]
    pub struct Task{
        pub title: String,
        pub done: bool,
        pub desc: Option<String>,
    }

    impl Task {
        pub fn new(title: impl Into<String>) -> Task {
            Task {
                title: title.into(),
                done: false,
                desc: None
            }
        }
    }
    impl Default for Task {
        fn default() -> Self {
            Self { title: "Untitled".to_string(), done: false, desc: None }
        }
    }

    pub fn run() {
        // 1.
        let task = Task {
            title: "Task 01".to_string(),
            done: false,
            desc: None
        };
        println!("{task:#?}");
        // 2.
        let task = Task::new("Task 02");
        println!("{task:#?}");
        // 3.
        let task = Task::default();
        println!("{task:#?}");
        // 4.
        let task: Option<Task> = None;
        let task = task.unwrap_or_default();
        println!("{task:#?}");
        // 5.
        let task = Task {
            done: true,
            ..Default::default()
        };
        println!("{task:#?}");
        // 6. 
        let task = Task {
            desc: Some("Description".to_string()),
            ..Task::new("Task 06")
        };
        println!("{task:#?}");
    }

}

mod builder_pattern {

    #[derive(Debug)]
    struct Request {
        pub url: String,
        pub method: String, // should be enum
        pub headres: Vec<(String, String)>, // (name, value)
        pub body: Option<String>,
    }

    #[derive(Default)]
    struct RequestBuilder {
        pub url: Option<String>,
        pub method: Option<String>, // should be enum
        pub headers: Vec<(String, String)>, // (name, value)
        pub body: Option<String>,
    }
    impl RequestBuilder {
        pub fn new() -> Self {
            RequestBuilder::default()
        }
        pub fn url(&mut self, url: impl Into<String>) -> &mut Self {
            self.url = Some(url.into());
            self
        }
        pub fn method(&mut self, method: impl Into<String>) -> &mut Self {
            self.method = Some(method.into());
            self
        }
        pub fn body(&mut self, body: impl Into<String>) -> &mut Self {
            self.body = Some(body.into());
            self
        }
        pub fn header(&mut self, name: impl Into<String>, value: impl Into<String>) -> &mut Self {
            self.headers.push((name.into(), value.into()));
            self
        }
        pub fn build(&self) -> Result<Request, ()> {
            let Some(url) = self.url.as_ref() else {
                return Err(());
            };
            let method = self.method
            .as_ref().cloned()
            .unwrap_or_else(|| "GET".to_string());
            Ok( Request { 
                url: url.to_string(),
                method,
                headres: self.headers.clone(),
                body: self.body.clone()
            })
        }    
    }
    pub fn run() {
        let req = RequestBuilder::new()
            .url("https://some-url.com/task/123")
            .method("GET")
            .header("token", "user_uuid.exp.sign")
            .build().unwrap();
        println!("{req:#?}");
    }
}

mod builder_pattern_2 {

    #[derive(Debug)]
    struct Request {
        pub url: String,
        pub method: String, // should be enum
        pub headres: Vec<(String, String)>, // (name, value)
        pub body: Option<String>,
    }

    #[derive(Default, Clone)]
    struct RequestBuilder {
        pub url: Option<String>,
        pub method: Option<String>, // should be enum
        pub headers: Vec<(String, String)>, // (name, value)
        pub body: Option<String>,
    }

    impl RequestBuilder {
        pub fn new() -> Self {
            RequestBuilder::default()
        }
        pub fn url(mut self, url: impl Into<String>) -> Self {
            self.url = Some(url.into());
            self
        }
        pub fn method(mut self, method: impl Into<String>) -> Self {
            self.method = Some(method.into());
            self
        }
        pub fn body(mut self, body: impl Into<String>) -> Self {
            self.body = Some(body.into());
            self
        }
        pub fn header(mut self, name: impl Into<String>, value: impl Into<String>) -> Self {
            self.headers.push((name.into(), value.into()));
            self
        }
        pub fn build(self) -> Result<Request, ()> {
            let Some(url) = self.url.as_ref() else {
                return Err(());
            };
            let method = self.method
            .as_ref().cloned()
            .unwrap_or_else(|| "GET".to_string());
            Ok( Request { 
                url: url.to_string(),
                method,
                headres: self.headers.clone(),
                body: self.body.clone()
            })
        }    
    }

    pub fn run() {
        let req_builder = RequestBuilder::new()
            .url("https://some-url.com/task/123")
            .method("GET")
            .header("token", "user_uuid.exp.sign");
        let req = req_builder
            .clone().build().unwrap(); 
        println!("{req:#?}");

        let req = req_builder
            .header("Client-VErsion", "1.2")
            .clone().build().unwrap();
        println!("{req:#?}");
    }
}

mod simple_pattern {
    pub fn run() {

    }
}
fn main() {
    run();
}
