
fn main() {
    let dialog = initialize();
    dialog.render();
    dialog.refresh();
}

pub trait Button {
    fn render(&self);
    fn on_click(&self);
}

pub struct HtmlButton;
pub struct WindowsButton;

impl Button for HtmlButton {
    fn render(&self) {
        println!("<button>Test Button</button>");
        self.on_click();
    }
    fn on_click(&self) {
        println!("Click! Hello Html!")
    }
}

impl Button for WindowsButton {
    fn render(&self) {
        println!("<windows>Test Button</windows>");
        self.on_click();
    }
    fn on_click(&self) {
        println!("Click! Hello Windows!")
    }
}

pub struct HtmlDialog;
pub struct WindowsDialog;

pub trait Dialog {
    fn create_button(&self) -> Box<dyn Button>;
    fn render(&self) {
        let button = self.create_button();
        button.render();
    }
    fn refresh(&self) {
        println!("Dialog - Refresh");
    }
}

impl Dialog for HtmlDialog {
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(HtmlButton)
    }
}

impl Dialog for WindowsDialog {
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(WindowsButton)
    }
}

pub fn initialize() -> &'static dyn Dialog {
    if cfg!(windows) {
        &WindowsDialog
    } else if cfg!(target_os = "linux") {
        &WindowsDialog
    } else {
        &HtmlDialog
    }
}

